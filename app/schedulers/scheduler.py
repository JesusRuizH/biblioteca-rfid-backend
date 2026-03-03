import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
from app.core.config import settings
from app.services.email_service import send_email
from datetime import datetime, timedelta, timezone
import asyncio
from zoneinfo import ZoneInfo



logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

# Token en memoria, se renueva al iniciar
admin_token = None

async def get_admin_token():
    global admin_token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.POCKETBASE_URL}/api/collections/_superusers/auth-with-password",
            json={
                "identity": settings.POCKETBASE_EMAIL,
                "password": settings.POCKETBASE_PASSWORD
            }
        )
        response.raise_for_status()
        admin_token = response.json().get("token")
        logger.info("Token de admin obtenido correctamente")

async def check_expiring_loans():
    logger.info("Revisando préstamos próximos a vencer...")
    # Si por alguna razón no hay token, intentar obtenerlo
    if not admin_token:
        await get_admin_token()

    mexico_tz = ZoneInfo("America/Mexico_City")

    now_mexico = datetime.now(mexico_tz)
    tomorrow_str = (now_mexico + timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.POCKETBASE_URL}/api/collections/Prestamos/records",
                params={
                    "filter": f'fecha_entrega >= "{tomorrow_str} 00:00:00" && fecha_entrega <= "{tomorrow_str} 23:59:59" && estatus_entrega = false',
                    "expand": "fk_id_usuario",
                    "perPage": 500
                },
                headers={
                    "Authorization": f"Bearer {admin_token}"
                }
            )
            response.raise_for_status()
            data = response.json()
            loans = data.get("items", [])
            logger.info(f"Préstamos por vencer mañana: {len(loans)}")

    except Exception as e:
        logger.error(f"Error consultando PocketBase: {str(e)}")
        return

    

    for loan in loans:
        try:
            user = loan.get("expand", {}).get("fk_id_usuario", {})
            user_email = user.get("email")
            user_name = user.get("nombre_usuario", "Usuario")
            fecha_entrega = loan.get("fecha_entrega", "")[:10]

            if not user_email:
                logger.warning(f"Préstamo {loan.get('id')} sin email de usuario, se omite")
                continue

            body_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            </head>
            <body style="margin:0; padding:0; background-color:#f4f4f4; font-family: Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding: 40px 0;">
                <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:8px; overflow:hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background-color:#1a237e; padding: 30px 40px; text-align:center;">
                        <h1 style="color:#ffffff; margin:0; font-size:24px;">📚 Biblioteca RFID</h1>
                        </td>
                    </tr>

                    <!-- Alerta -->
                    <tr>
                        <td style="background-color:#fff3e0; padding: 16px 40px; border-left: 4px solid #ff6f00;">
                        <p style="margin:0; color:#e65100; font-weight:bold; font-size:15px;">⚠️ Recordatorio de entrega</p>
                        </td>
                    </tr>

                    <!-- Contenido -->
                    <tr>
                        <td style="padding: 32px 40px;">
                        <p style="color:#333333; font-size:16px; margin-top:0;">Hola <strong>{user_name}</strong>,</p>
                        <p style="color:#555555; font-size:15px; line-height:1.6;">
                            Te informamos que tienes un préstamo activo cuya fecha de entrega es <strong>mañana</strong>.
                            Por favor devuelve el material a tiempo para evitar penalizaciones.
                        </p>

                        <!-- Tarjeta de info -->
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f8f9fa; border-radius:6px; margin: 24px 0;">
                            <tr>
                            <td style="padding: 20px 24px;">
                                <p style="margin:0 0 8px 0; color:#888; font-size:13px; text-transform:uppercase; letter-spacing:1px;">Fecha límite de entrega</p>
                                <p style="margin:0; color:#1a237e; font-size:22px; font-weight:bold;">📅 {fecha_entrega}</p>
                            </td>
                            </tr>
                        </table>

                        <p style="color:#555555; font-size:15px; line-height:1.6;">
                            Si ya realizaste la devolución, puedes ignorar este mensaje.
                        </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color:#f8f9fa; padding: 20px 40px; border-top: 1px solid #eeeeee; text-align:center;">
                        <p style="margin:0; color:#aaaaaa; font-size:12px;">
                            Este es un mensaje automático, por favor no respondas a este correo.<br>
                            © 2026 Biblioteca RFID
                        </p>
                        </td>
                    </tr>

                    </table>
                </td>
                </tr>
            </table>
            </body>
            </html>
            """

            success = send_email(
                to=user_email,
                subject="⚠️ Recordatorio: tu préstamo vence mañana",
                body_html=body_html
            )

            if success:
                logger.info(f"Recordatorio enviado a {user_email} para préstamo {loan.get('id')}")

        except Exception as e:
            logger.error(f"Error procesando préstamo {loan.get('id')}: {str(e)}")
            continue

def start_scheduler():
    scheduler.add_job(
        check_expiring_loans,
        trigger="cron",
        hour=9,
        minute=0,
        id="check_expiring_loans",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler iniciado")