from dataclasses import dataclass
from dataclasses import field, asdict
from typing import List, Dict, Optional


@dataclass
class TextBlock:
    text: str
    type: str = "plain_text"
    emoji: bool = True


@dataclass
class HeaderBlock:
    text: TextBlock
    type: str = field(default="header", init=False)


@dataclass
class Action:
    type: str = field(default="actions", init=False)
    elements: List = field(default_factory=list)


@dataclass
class Option:
    text: TextBlock
    value: str


@dataclass
class StaticSelect:
    type: str = field(default="static_select", init=False)
    placeholder: TextBlock
    action_id: str
    options: List[Option] = field(default_factory=list)


@dataclass
class Button:
    type: str = field(default="button", init=False)
    text: TextBlock
    action_id: str


@dataclass
class Element:
    text: str
    type: str = "mrkdwn"


@dataclass
class ContextBlock:
    type: str = field(default="context", init=False)
    elements: List[Element] = field(default_factory=list)


@dataclass
class InputBlock:
    element: Dict
    label: TextBlock
    type: str = 'input'


@dataclass
class Checkbox:
    action_id: str
    options: List[Option] = field(default_factory=list)
    type: str = 'checkboxes'


@dataclass
class MultiUsersSelect:
    action_id: str
    placeholder: TextBlock
    type: str = 'multi_users_select'


@dataclass
class Section:
    text: Dict
    type: str = 'section'


@dataclass
class TemplateUIBlocks:
    blocks: List = field(default_factory=list)


def ui_scrum_pocker(title: str, users: Optional[List] = None) -> Dict:
    blocks = list()
    blocks.append(HeaderBlock(TextBlock(title)))
    if users:
        blocks.append(
            ContextBlock([Element(
                f"<@{user}> {grade} ") for user, grade in users.items()])
        )

    blocks.append(
        Action(
            [
                StaticSelect(
                    placeholder=TextBlock(
                        "оценка задачи",
                    ),
                    options=[
                        Option(TextBlock(f"{item}"), f"{item}")
                        for item in [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ":coffee:"]
                    ],
                    action_id="static_select-action",
                ),
                Button(
                    text=TextBlock(
                        "show me",
                    ),
                    action_id="action_click",
                ),
            ]
        )
    )

    obj = TemplateUIBlocks(blocks=blocks)
    return asdict(obj)


def ui_elections():
    blocks = [
        HeaderBlock(
            TextBlock(
                "бот для выбора ведущих мероприятия"
            )),
        InputBlock(
            element=MultiUsersSelect(
                placeholder=TextBlock("выбрать участников"),
                action_id="multi_users_select-action"
            ),
            label=TextBlock(
                "команда"
            )
        ),
        Action(
            elements=[
                Checkbox(
                    options=[
                        Option(text=TextBlock("ведущий"), value="mentor"),
                        Option(text=TextBlock("ответственный за каденции"), value="caden"),
                        Option(text=TextBlock("ответственный за экран"), value="screen")
                    ],
                    action_id="checkboxes-action"
                ),
                Button(
                    text=TextBlock("запуск"),
                    action_id="election_button-action"
                )
            ]
        )
    ]
    obj = TemplateUIBlocks(blocks=blocks)
    return asdict(obj)


def ui_elections_result(text: str):
    blocks = [
        HeaderBlock(TextBlock("на мероприятии")),
        Section(text={'type': 'mrkdwn', 'text': text})
    ]
    obj = TemplateUIBlocks(blocks)
    return asdict(obj)
