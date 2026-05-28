from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty

# ==============================================================================
# БЛОК ВХОДНЫХ ДАННЫХ (Редактируй эти цифры перед сборкой)
# ==============================================================================
TOTAL_GOAL = 1000000
TOTAL_CURRENT = 350000

# Данные по неделям (Название, План, Факт)
WEEKLY_DATA = [
    {"name": "Неделя 1", "goal": 25000, "current": 25000},
    {"name": "Неделя 2", "goal": 25000, "current": 21000},
    {"name": "Неделя 3", "goal": 25000, "current": 12000},
    {"name": "Неделя 4", "goal": 25000, "current": 0},
]
# ==============================================================================

# Разметка интерфейса на языке KV (Декларативное описание дизайна)
KV = '''
MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: 0.97, 0.98, 0.99, 1  # Светлый фон экрана

    MDTopAppBar:
        title: "Мониторинг марафона"
        elevation: 2
        md_bg_color: 0.05, 0.09, 0.16, 1  # Темно-синий верхний бар
        specific_text_color: 1, 1, 1, 1

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True

        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            padding: dp(16)
            spacing: dp(24)

            # Карточка главного круга
            MDCard:
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(16)
                radius: [12, 12, 12, 12]
                elevation: 1
                md_bg_color: 1, 1, 1, 1

                MDLabel:
                    text: "Общий прогресс цели"
                    font_style: "H6"
                    bold: True
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.1, 0.15, 0.25, 1

                MDBoxLayout:
                    orientation: 'horizontal'
                    adaptive_height: True
                    spacing: dp(16)
                    padding: [0, dp(16), 0, 0]

                    # Контейнер для круговой шкалы
                    AnchorLayout:
                        anchor_x: 'center'
                        anchor_y: 'center'
                        size_hint: (None, None)
                        size: (dp(120), dp(120))
                        
                        DonutChart:
                            id: main_donut
                            size_hint: (None, None)
                            size: (dp(120), dp(120))

                    # Текстовые метрики рядом с кругом
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        pos_hint: {"center_y": .5}

                        MDLabel:
                            id: lbl_percent
                            text: "0.0%"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.05, 0.65, 0.91, 1  # Голубой акцент

                        MDLabel:
                            id: lbl_absolute
                            text: "0 / 0"
                            font_style: "Body2"
                            theme_text_color: "Secondary"

            # Карточка недельных шкал
            MDCard:
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(16)
                radius: [12, 12, 12, 12]
                elevation: 1
                md_bg_color: 1, 1, 1, 1

                MDLabel:
                    text: "Оперативные спринты"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.1, 0.15, 0.25, 1
                    
                MDBoxLayout:
                    id: weeks_container
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(18)
                    padding: [0, dp(16), 0, 0]

# Шаблон для динамических строк с недельными прогресс-барами
<WeeklyRow@MDBoxLayout>:
    orientation: 'vertical'
    adaptive_height: True
    spacing: dp(4)
    w_name: ""
    w_info: ""
    w_progress: 0
    w_color: [0.23, 0.51, 0.96, 1]

    MDBoxLayout:
        orientation: 'horizontal'
        adaptive_height: True
        MDLabel:
            text: root.w_name
            bold: True
            font_style: "Body1"
        MDLabel:
            text: root.w_info
            halign: "right"
            font_style: "Caption"
            theme_text_color: "Secondary"

    MDProgressBar:
        value: root.w_progress
        max: 100
        color: root.w_color
        back_color: [0.88, 0.91, 0.94, 1]
'''

# Класс кастомного виджета для ручной отрисовки круговой шкалы (Donut) через Canvas
class DonutChart(Widget):
    progress = NumericProperty(0)

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # 1. Фоновый круг (серый остаток)
            Color(0.88, 0.91, 0.94, 1)
            Ellipse(pos=self.pos, size=self.size)
            
            # 2. Сектор текущего прогресса
            if self.progress > 0:
                # Если цель закрыта на 100% — красим в зеленый, иначе в голубой
                if self.progress >= 100:
                    Color(0.06, 0.73, 0.51, 1)
                else:
                    Color(0.05, 0.65, 0.91, 1)
                
                # Математический расчет секторов угла для корректного хода часов
                angle_size = (self.progress / 100.0) * 360
                Ellipse(pos=self.pos, size=self.size, angle_start=360-angle_size, angle_end=360)
            
            # 3. Внутренний маскирующий круг (вырезает центр, превращая круг в кольцо)
            Color(1, 1, 1, 1)
            padding = self.width * 0.16
            Ellipse(pos=(self.x + padding/2, self.y + padding/2), 
                    size=(self.width - padding, self.height - padding))

class MarathonApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        # Расчет данных для главного кольца прогресса
        percent = (TOTAL_CURRENT / TOTAL_GOAL) * 100 if TOTAL_GOAL > 0 else 0
        self.root.ids.main_donut.progress = min(100, percent)
        self.root.ids.main_donut.draw()
        
        self.root.ids.lbl_percent.text = f"{percent:.1f}%"
        self.root.ids.lbl_absolute.text = f"{TOTAL_CURRENT:,} из {TOTAL_GOAL:,}"

        # Динамическая генерация недельных шкал на основе массива WEEKLY_DATA
        from kivy.factory import Factory
        for week in WEEKLY_DATA:
            w_pct = (week["current"] / week["goal"]) * 100 if week["goal"] > 0 else 0
            w_pct_capped = min(100, w_pct)
            
            # Цветовой маркер: выполненная неделя — зеленая, текущая — синяя
            color = [0.06, 0.73, 0.51, 1] if w_pct >= 100 else [0.23, 0.51, 0.96, 1]
            
            row = Factory.WeeklyRow()
            row.w_name = week["name"]
            row.w_info = f"{week['current']:,} / {week['goal']:,} ({w_pct:.1f}%)"
            row.w_progress = w_pct_capped
            row.w_color = color
            
            self.root.ids.weeks_container.add_widget(row)

if __name__ == '__main__':
    MarathonApp().run()