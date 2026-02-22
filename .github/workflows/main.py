from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random

# 全局背景
Window.clearcolor = get_color_from_hex("#F5F9FF")

# ====================== 整本教材单词库（已内置）======================
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

# ====================== 主APP（完整版）======================
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
        main = BoxLayout(orientation='vertical', padding=25, spacing=12)

        # 标题
        main.add_widget(Label(
            text="📘 英语听写学习机",
            font_size=30,
            color=get_color_from_hex("#2C3E50"),
            size_hint_y=0.15
        ))

        # 1. 选择年级
        self.spn_grade = Spinner(
            text="选择年级",
            values=list(word_database.keys()),
            size_hint_y=0.12
        )
        main.add_widget(self.spn_grade)

        # 2. 选择教材版本
        self.spn_version = Spinner(
            text="选择教材",
            values=[],
            size_hint_y=0.12
        )
        main.add_widget(self.spn_version)

        # 3. 选择单元
        self.spn_unit = Spinner(
            text="选择单元/全书",
            values=[],
            size_hint_y=0.12
        )
        main.add_widget(self.spn_unit)

        # 功能按钮
        main.add_widget(Button(
            text="🎯 入学测试（自动制定计划）",
            background_color=get_color_from_hex("#FF6B6B"),
            size_hint_y=0.12,
            on_press=self.start_test
        ))
        main.add_widget(Button(
            text="▶️ 开始听写",
            background_color=get_color_from_hex("#4ECDC4"),
            size_hint_y=0.12,
            on_press=self.start_dictation
        ))
        main.add_widget(Button(
            text="📖 打开课本",
            background_color=get_color_from_hex("#FFD166"),
            size_hint_y=0.12,
            on_press=self.show_book
        ))

        # 中文提示（要听写的单词意思）
        self.word_label = Label(
            text="请选择单元开始学习",
            font_size=22,
            color=get_color_from_hex("#34495E"),
            size_hint_y=0.15
        )
        main.add_widget(self.word_label)

        # 字母提示
        self.hint_label = Label(
            text="💡 提示区",
            font_size=18,
            color=get_color_from_hex("#7F8C8D"),
            size_hint_y=0.12
        )
        main.add_widget(self.hint_label)

        # 输入框
        self.input = TextInput(
            hint_text="在这里输入单词拼写",
            font_size=20,
            size_hint_y=0.18,
            padding=15
        )
        main.add_widget(self.input)

        # 播放 + 提示 + 提交
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
        main.add_widget(bottom_bar)

        # 联动选择
        self.spn_grade.bind(text=self.on_grade_change)
        self.spn_version.bind(text=self.on_version_change)

        return main

    # ===================== 功能实现 =====================
    def on_grade_change(self, *args):
        self.grade = self.spn_grade.text
        self.spn_version.values = list(word_database[self.grade].keys())

    def on_version_change(self, *args):
        self.version = self.spn_version.text
        self.spn_unit.values = list(word_database[self.grade][self.version].keys())

    def start_dictation(self, *args):
        self.unit = self.spn_unit.text
        self.words = word_database[self.grade][self.version][self.unit]
        self.index = 0
        self.test_mode = False
        self.show_current()

    def start_test(self, *args):
        self.unit = self.spn_unit.text
        self.words = word_database[self.grade][self.version]["全书单词"].copy()
        random.shuffle(self.words)
        self.words = self.words[:10]
        self.index = 0
        self.score = 0
        self.test_mode = True
        self.show_current()

    def show_current(self):
        w = self.words[self.index]
        self.word_label.text = f"请拼写：{w['cn']}"
        self.input.text = ""
        self.hint_label.text = "💡 提示区"

    def play_word(self, instance):
        if self.words:
            pass  # 手机端可扩展音频功能，不影响打包

    def give_hint(self, instance):
        if not self.words:
            return
        w = self.words[self.index]['en']
        if len(w) >= 2:
            self.hint_label.text = f"💡 提示：{w[:2]} ____"
        else:
            self.hint_label.text = f"💡 提示：{w[0]} ___"

    def check_answer(self, instance):
        if not self.words:
            return
        w = self.words[self.index]
        user = self.input.text.strip().lower()
        ans = w['en'].lower()

        if user == ans:
            self.word_label.text = "✅ 回答正确！"
            if self.test_mode:
                self.score += 1
        else:
            self.word_label.text = f"❌ 正确：{w['en']}"

        self.index += 1
        if self.index < len(self.words):
            self.show_current()
        else:
            if self.test_mode:
                total = len(self.words)
                correct = self.score
                rate = correct / total
                if rate >= 0.8:
                    res = f"🎯 测试完成！{correct}/{total}\n建议难度：提高版"
                elif rate >= 0.5:
                    res = f"🎯 测试完成！{correct}/{total}\n建议难度：标准班"
                else:
                    res = f"🎯 测试完成！{correct}/{total}\n建议难度：基础班"
                self.word_label.text = res
            else:
                self.word_label.text = "🎉 本课学习完成！"

    def show_book(self, instance):
        self.word_label.text = "📖 教材已打开（可在课本中找答案）\nUnit 单词均来自课本原文"

if __name__ == "__main__":
    EnglishDictationApp().run()