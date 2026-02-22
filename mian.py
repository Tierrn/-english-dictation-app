from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random

# 设置APP背景色
Window.clearcolor = get_color_from_hex("#F5F9FF")

# 内置单词库（一年级人教版）
word_database = {
    "一年级": {
        "人教版": {
            "Unit 1": [
                {"en": "apple", "cn": "苹果"},
                {"en": "banana", "cn": "香蕉"},
                {"en": "cat", "cn": "猫"},
                {"en": "dog", "cn": "狗"},
            ],
            "Unit 2": [
                {"en": "egg", "cn": "鸡蛋"},
                {"en": "fish", "cn": "鱼"},
                {"en": "goat", "cn": "山羊"},
                {"en": "hat", "cn": "帽子"},
            ],
            "全书单词": [
                {"en": "apple", "cn": "苹果"},
                {"en": "banana", "cn": "香蕉"},
                {"en": "cat", "cn": "猫"},
                {"en": "dog", "cn": "狗"},
                {"en": "egg", "cn": "鸡蛋"},
                {"en": "fish", "cn": "鱼"},
                {"en": "goat", "cn": "山羊"},
                {"en": "hat", "cn": "帽子"},
            ]
        }
    }
}

# 主APP类
class EnglishDictationApp(App):
    def build(self):
        self.grade = None
        self.version = None
        self.unit = None
        self.words = []
        self.index = 0
        self.test_mode = False
        self.score = 0

        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=25, spacing=12)

        # 标题
        main_layout.add_widget(Label(
            text="📘 英语听写学习机",
            font_size=30,
            color=get_color_from_hex("#2C3E50"),
            size_hint_y=0.15
        ))

        # 年级选择器
        self.grade_spinner = Spinner(
            text="选择年级",
            values=list(word_database.keys()),
            size_hint_y=0.12
        )
        main_layout.add_widget(self.grade_spinner)

        # 教材版本选择器
        self.version_spinner = Spinner(
            text="选择教材",
            values=[],
            size_hint_y=0.12
        )
        main_layout.add_widget(self.version_spinner)

        # 单元选择器
        self.unit_spinner = Spinner(
            text="选择单元/全书",
            values=[],
            size_hint_y=0.12
        )
        main_layout.add_widget(self.unit_spinner)

        # 功能按钮
        main_layout.add_widget(Button(
            text="🎯 入学测试（自动制定计划）",
            background_color=get_color_from_hex("#FF6B6B"),
            size_hint_y=0.12,
            on_press=self.start_test
        ))
        main_layout.add_widget(Button(
            text="▶️ 开始听写",
            background_color=get_color_from_hex("#4ECDC4"),
            size_hint_y=0.12,
            on_press=self.start_dictation
        ))
        main_layout.add_widget(Button(
            text="📖 打开课本",
            background_color=get_color_from_hex("#FFD166"),
            size_hint_y=0.12,
            on_press=self.show_book
        ))

        # 单词中文提示
        self.word_label = Label(
            text="请选择单元开始学习",
            font_size=22,
            color=get_color_from_hex("#34495E"),
            size_hint_y=0.15
        )
        main_layout.add_widget(self.word_label)

        # 字母提示区
        self.hint_label = Label(
            text="💡 提示区",
            font_size=18,
            color=get_color_from_hex("#7F8C8D"),
            size_hint_y=0.12
        )
        main_layout.add_widget(self.hint_label)

        # 输入框
        self.input_box = TextInput(
            hint_text="在这里输入单词拼写",
            font_size=20,
            size_hint_y=0.18,
            padding=15
        )
        main_layout.add_widget(self.input_box)

        # 底部操作栏
        bottom_bar = BoxLayout(size_hint_y=0.15, spacing=8)
        bottom_bar.add_widget(Button(
            text="播放读音",
            background_color=get_color_from_hex("#51CF66"),
            on_press=self.play_word
        ))
        bottom_bar.add_widget(Button(
            text="字母提示",
            background_color=get_color_from_hex("#9775FA"),
            on_press=self.give_hint
        ))
        bottom_bar.add_widget(Button(
            text="提交答案",
            background_color=get_color_from_hex("#228BE6"),
            on_press=self.check_answer
        ))
        main_layout.add_widget(bottom_bar)

        # 联动选择器（选年级后自动加载教材，选教材后加载单元）
        self.grade_spinner.bind(text=self.on_grade_change)
        self.version_spinner.bind(text=self.on_version_change)

        return main_layout

    # 年级选择联动
    def on_grade_change(self, *args):
        self.grade = self.grade_spinner.text
        self.version_spinner.values = list(word_database[self.grade].keys())

    # 教材版本选择联动
    def on_version_change(self, *args):
        self.version = self.version_spinner.text
        self.unit_spinner.values = list(word_database[self.grade][self.version].keys())

    # 开始听写
    def start_dictation(self, *args):
        self.unit = self.unit_spinner.text
        self.words = word_database[self.grade][self.version][self.unit]
        self.index = 0
        self.test_mode = False
        self.show_current_word()

    # 开始入学测试（随机10个单词）
    def start_test(self, *args):
        self.unit = self.unit_spinner.text
        self.words = word_database[self.grade][self.version]["全书单词"].copy()
        random.shuffle(self.words)
        self.words = self.words[:10]
        self.index = 0
        self.score = 0
        self.test_mode = True
        self.show_current_word()

    # 显示当前要听写的单词
    def show_current_word(self):
        current_word = self.words[self.index]
        self.word_label.text = f"请拼写：{current_word['cn']}"
        self.input_box.text = ""
        self.hint_label.text = "💡 提示区"

    # 播放单词读音（预留接口，不影响打包）
    def play_word(self, instance):
        if self.words:
            pass

    # 给出字母提示
    def give_hint(self, instance):
        if not self.words:
            return
        en_word = self.words[self.index]['en']
        if len(en_word) >= 2:
            self.hint_label.text = f"💡 提示：{en_word[:2]} ____"
        else:
            self.hint_label.text = f"💡 提示：{en_word[0]} ___"

    # 检查答案
    def check_answer(self, instance):
        if not self.words:
            return
        current_word = self.words[self.index]
        user_answer = self.input_box.text.strip().lower()
        correct_answer = current_word['en'].lower()

        # 判断对错
        if user_answer == correct_answer:
            self.word_label.text = "✅ 回答正确！"
            if self.test_mode:
                self.score += 1
        else:
            self.word_label.text = f"❌ 正确答案：{current_word['en']}"

        # 切换下一个单词
        self.index += 1
        if self.index < len(self.words):
            self.show_current_word()
        else:
            # 测试完成显示结果
            if self.test_mode:
                total = len(self.words)
                correct = self.score
                accuracy = correct / total
                if accuracy >= 0.8:
                    result = f"🎯 测试完成！{correct}/{total}\n建议难度：提高版"
                elif accuracy >= 0.5:
                    result = f"🎯 测试完成！{correct}/{total}\n建议难度：标准版"
                else:
                    result = f"🎯 测试完成！{correct}/{total}\n建议难度：基础版"
                self.word_label.text = result
            else:
                self.word_label.text = "🎉 本课学习完成！"

    # 打开课本提示
    def show_book(self, instance):
        self.word_label.text = "📖 教材已打开（单词均来自课本原文）\n可对照课本核对拼写"

if __name__ == "__main__":
    EnglishDictationApp().run()
