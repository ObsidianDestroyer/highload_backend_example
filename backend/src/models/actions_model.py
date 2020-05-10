import typing as t

from tortoise import Model, fields


class Actions(Model):
    id = fields.IntField(pk=True)
    path = fields.CharField(max_length=128, unique=False)
    user = fields.ForeignKeyField(
        'models.User',
        related_name='user_actions',
        on_delete='CASCADE',
        to_field='uid',
    )
    # Just for simplicity
    act_VIEW = fields.IntField(default=0)
    act_READ = fields.IntField(default=0)
    act_CLICK = fields.IntField(default=0)
    act_SCROLL = fields.IntField(default=0)
    act_CHECKOUT = fields.IntField(default=0)

    async def update_action_count(self, name: str) -> None:
        """
        Increments ACTION counter by +one
        :param name:
        :return:
        """
        action_attr = f'act_{name}'
        updated_value = getattr(self, action_attr) + 1
        setattr(self, action_attr, updated_value)
        await self.save()
        return getattr(self, action_attr)

    def get_actions(self) -> t.List[dict]:
        """
            Rendering actions
            :return:
        """
        return [
            {action.strip('act_'): getattr(self, action)}
            for action in self.__dir__()
            if 'act_' in action
        ]

    def render(self) -> dict:
        return {'path': self.path, 'actions': self.get_actions()}
