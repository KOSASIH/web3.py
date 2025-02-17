from celery import Celery
from celery.utils.log import get_task_logger
import time
import random

# Initialize Celery
celery = Celery('pi_coin', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Set up logging
logger = get_task_logger(__name__)

@celery.task(bind=True, max_retries=5, default_retry_delay=10)
def update_user_balance(self, user_id, amount):
    """
    Update the balance of a user. This task simulates a delay and can fail randomly
    to demonstrate retry functionality.
    
    :param user_id: ID of the user whose balance is to be updated
    :param amount: Amount to add to the user's balance
    """
    try:
        # Simulate a random failure
        if random.choice([True, False]):
            raise ValueError("Simulated failure for demonstration purposes.")
        
        # Simulate a delay for processing
        time.sleep(2)
        
        # Here you would normally update the user's balance in the database
        logger.info(f"User {user_id} balance updated by {amount}.")
        
        # Return success message
        return f"User {user_id} balance updated successfully by {amount}."
    
    except Exception as exc:
        logger.error(f"Error updating balance for user {user_id}: {exc}")
        # Retry the task if it fails
        raise self.retry(exc=exc)

@celery.task
def send_notification(user_id, message):
    """
    Send a notification to the user. This task simulates sending a notification.
    
    :param user_id: ID of the user to notify
    :param message: Notification message
    """
    # Simulate a delay for sending notification
    time.sleep(1)
    logger.info(f"Notification sent to user {user_id}: {message}")
    return f"Notification sent to user {user_id}."

@celery.task
def process_transaction(user_id, amount):
    """
    Process a transaction for a user. This task combines updating the balance
    and sending a notification.
    
    :param user_id: ID of the user
    :param amount: Amount to process
    """
    logger.info(f"Processing transaction for user {user_id} with amount {amount}.")
    
    # Update user balance
    update_user_balance.delay(user_id, amount)
    
    # Send notification
    send_notification.delay(user_id, f"Your balance has been updated by {amount}.")

# Example of a periodic task (optional)
@celery.task
def periodic_task():
    """
    A periodic task that runs every minute.
    """
    logger.info("Periodic task executed.")
