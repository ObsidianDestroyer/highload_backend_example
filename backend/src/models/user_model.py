from tortoise import fields
from tortoise.models import Model

from backend.src.models import Actions


class User(Model):
    uid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128, required=True)
    actions: fields.ForeignKeyRelation[Actions]

    @property
    def UID(self):
        return str(self.uid)

    async def render(self) -> dict:
        actions = await Actions.filter(user=self).all()
        return {
            'UID': str(self.uid),
            'userName': self.name,
            'userActions': [action.render() for action in actions],
        }
