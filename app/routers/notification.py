from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, get_current_user, CurrentUser

router = APIRouter(prefix="/api/v1/notification", tags=["Notification"])

# --- Helper de permisos ---

def _check_access_to_user(target_user_id: int, current_user: CurrentUser):
    """
    Solo el propio usuario o un ADMIN pueden ver/borrar notificaciones.
    """
    if current_user.id != target_user_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

# --- POST (opcional) para crear notificaciones ---

@router.post(
    "",
    response_model=schemas.NotificationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    payload: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Opcional: crea una notificación.
    - Si no envías user_id en el body, se le crea al usuario autenticado.
    - Si envías otro user_id, solo debería poder hacerlo un ADMIN u otro servicio.
    """
    target_user_id = payload.user_id or current_user.id

    if target_user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions to create for others")

    notif = models.Notification(
        title=payload.title,
        description=payload.description,
        user_id=target_user_id,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

# --- GET /api/v1/notification/{userId} ---

@router.get("/{user_id}", response_model=list[schemas.NotificationOut])
def get_notifications_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Devuelve todas las notificaciones de un usuario.
    Solo las puede ver él mismo o un ADMIN.
    """
    _check_access_to_user(user_id, current_user)

    notifs = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.id.desc())
        .all()
    )
    return notifs

# --- DELETE /api/v1/notification/{notificationId} ---

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    notif = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id)
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    _check_access_to_user(notif.user_id, current_user)

    db.delete(notif)
    db.commit()
    return
