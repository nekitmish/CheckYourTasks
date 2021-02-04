from .health import HealthEndpoint
from .base import BaseEndpoint
from .employees.create import CreateEmployeeEndpoint
from .employees.get_all import AllEmployeeEndpoint
from .employees.auth import AuthEmployeeEndpoint
from .employees.employee import EmployeeEndpoint
from .employees.my_employee import MyEmployeeEndpoint
from .employees.my_employee_by_login import GetMyEmployeeByLoginEndpoint

from .messages.message import MessageEndpoint
from .messages.message_actions import MessageActionEndpoint
from .messages.messages_by_sender_login import SortMessagesBySenderLoginEndpoint
from .messages.messages_by_sender_id import SortMessagesBySenderIDEndpoint
from .messages.messages_by_recipient_login import SortMessagesByRecipientLoginEndpoint
from .messages.messages_by_recipient_id import SortMessagesByRecipientIDEndpoint


