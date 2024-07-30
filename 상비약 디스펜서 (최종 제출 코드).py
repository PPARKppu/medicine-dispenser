from tkinter import*
import RPi.GPIO as GPIO
import time

win = Tk()  # GUI 변수 정의

# GUI 기본 정보들
win.geometry("800x480")
win.title("상비약 자판기")
win.option_add("*Font", "함초롬돋움 25")
win.configure(bg="lightgreen")

history = []            # stack
user_selection_map = {} # 딕셔너리로 사용자 정보 저장
completed_users = []    # 설정 완료된 사용자 정보 저장
    

# GUI 설정
# 초기 사용자 정보 설정 화면
def show_user_buttons():
    clear_widgets() # 모든 윈도우 위젯 제거
    history.clear()
    history.append("user")
    label = Label(win, text="사용자 정보를 입력하세요.", font=("함초롬돋움", 15))
    label.pack()
    users = ["사용자1", "사용자2", "사용자3"]
    btn_width = 12
    btn_height = 3
    for user in users:
        if user not in completed_users:
            btn = Button(win, text=user, width=btn_width, height=btn_height, font=("함초롬돋움", 15), command=lambda u=user: select_user(u))
            btn.pack()
    complete_btn = Button(win, text="설정 완료", font=("함초롬돋움", 15), command=show_completed_users_screen)
    complete_btn.pack()

def select_user(user):
    if user not in user_selection_map:
        user_selection_map[user] = [None, None, None]
    show_gender_buttons(user)
    
# 성별 선택 화면
def show_gender_buttons(user):
    clear_buttons()
    history.append("gender")
    label = Label(win, text="성별을 선택하세요.", font=("함초롬돋움", 15))
    label.pack()
    genders = ["남자", "여자"]
    for gender in genders:
        btn = Button(win, text=gender, font=("함초롬돋움", 15), command=lambda g=gender: select_gender(user, g))
        btn.pack()
    add_nav_buttons()

def select_gender(user, gender):
    user_selection_map[user][1] = gender
    show_age_buttons(user)

# 나이 선택 화면
def show_age_buttons(user):
    clear_buttons()
    history.append("age")
    label = Label(win, text="나이를 선택하세요.", font=("함초롬돋움", 15))
    label.pack()
    ages = ["만 0~2세", "만 3~7세", "만 8~12세", "만 13~15세", "만 16세 이상"]
    for age in ages:
        btn = Button(win, text=age, font=("함초롬돋움", 15), command=lambda a=age: select_age(user, a))
        btn.pack()
    add_nav_buttons()

def select_age(user, age):
    user_selection_map[user][2] = age
    confirm_settings(user)

# 설정 완료 확인 화면
def confirm_settings(user):
    clear_buttons()
    history.append("confirm")
    label = Label(win, text="설정을 완료하시겠습니까?", font=("함초롬돋움", 15))
    label.pack()
    yes_btn = Button(win, text="예", font=("함초롬돋움", 15), command=lambda: complete_setup(user, label))
    yes_btn.pack()
    no_btn = Button(win, text="아니오", font=("함초롬돋움", 15), command=show_user_buttons)
    no_btn.pack()

def complete_setup(user, label):
    label.pack_forget()
    completed_users.append(user)
    show_user_buttons()

# 초기 설정에서 사용자 추가 마저 해야 할 때
def adding_user():
    clear_buttons()
    history.append("user")
    show_user_buttons()

# 초기 설정이 완료된 홈 화면
table_frame = None  # 전역 변수로 선언
def show_completed_users_screen():
    global table_frame  # 전역 변수로 사용

    clear_buttons()
    history.append("completed_users")

    if len(completed_users) == 0:
        show_user_buttons()
        return
   
    # 기존 테이블 프레임이 있으면 제거
    if table_frame:
        table_frame.destroy()
   
    # 표 형식으로 표시할 Frame 생성
    table_frame = Frame(win)
    table_frame.place(relx=0.5, rely=0.5, anchor="center")  # 중앙에 배치

    # 테이블 헤더 생성
    header1_label = Label(table_frame, text="사용자명", font=("함초롬돋움", 15, "bold"), padx=20, pady=10)
    header1_label.grid(row=0, column=0)
    header2_label = Label(table_frame, text="성별", font=("함초롬돋움", 15, "bold"), padx=20, pady=10)
    header2_label.grid(row=0, column=1)
    header3_label = Label(table_frame, text="나이", font=("함초롬돋움", 15, "bold"), padx=20, pady=10)
    header3_label.grid(row=0, column=2)

    # 사용자 정보 표시
    for index, user in enumerate(completed_users, start=1):
        user_info = user_selection_map[user]
        
        # 사용자명은 버튼으로 표시
        name_btn = Button(table_frame, text=user, font=("함초롬돋움", 13), command=lambda u=user: show_medication_buttons(u))
        name_btn.grid(row=index, column=0, padx=20, pady=10)

        # 성별은 텍스트로 표시
        gender_label = Label(table_frame, text=user_info[1], font=("함초롬돋움", 13))
        gender_label.grid(row=index, column=1, padx=20, pady=10)

        # 나이는 텍스트로 표시
        age_label = Label(table_frame, text=user_info[2], font=("함초롬돋움", 13))
        age_label.grid(row=index, column=2, padx=20, pady=10)

    # 사용자 추가 버튼
    add_user = Button(win, text="사용자 추가", font=("함초롬돋움", 13), command=adding_user)
    add_user.place(x=100, y=50)

    # 설정 초기화 버튼
    reset_btn = Button(win, text="설정 초기화", font=("함초롬돋움", 13), command=reset_settings)
    reset_btn.place(x=300, y=50)

    add_nav_buttons()

# 상비약/처방약/바코드 버튼 선택 화면
def show_medication_buttons(user):
    clear_widgets()
    history.append("medication")
    global user_selection_map
    user_inform = user_selection_map[user]
    btn1 = Button(win, text="상비약", width=10, font=("함초롬돋움", 15), command=lambda u=user_inform: show_symptom_button(u))
    btn1.pack()
    btn2 = Button(win, text="처방약", width=10, font=("함초롬돋움", 15), command=prescription_buttons)
    btn2.pack()
    qrbutton = Button(win, text="바코드 인식하기", width=15, font=("함초롬돋움", 15), command=barcode_scan)
    qrbutton.pack()
    add_nav_buttons()
    
def show_medication_buttons_with_label(label):
    label.pack_forget()
    show_medication_buttons()

# 설정 초기화 최종 확인 화면
def reset_settings():
    clear_widgets()
    history.append("reset")
    label = Label(win, text="설정을 리셋하시겠습니까?",  font=("함초롬돋움", 15))
    label.pack()
    yes_btn = Button(win, text="예", font=("함초롬돋움", 15), command=lambda: reset_to_initial(label))
    yes_btn.pack()
    no_btn = Button(win, text="아니오", font=("함초롬돋움", 15), command=lambda: show_completed_users_screen())
    no_btn.pack()

# 첫 초기 설정 화면으로
def reset_to_initial(label):
    label.pack_forget()
    global user_selection_map
    global completed_users
    user_selection_map = {}
    completed_users = []
    show_user_buttons()



# 상비약 기능
# 상비약 첫 페이지 (증상을 물음)
def show_symptom_button(user_inform):   
    clear_widgets()              
    history.append("symptom")
    symptom_btn = Button(win, text="증상은?", font=("함초롬돋움", 15), command=lambda u=user_inform: show_symptom_options(u)) 
    symptom_btn.pack()
    add_nav_buttons()

# 증상의 종류를 제시하는 화면
def show_symptom_options(user_inform):
    clear_widgets()
    history.append("symptom_options")
    symptoms = ["소화불량", "코감기", "목감기", "몸살", "알러지", "두드러기", "근육통", "두통", "타박상"]

    btn_width = 15
    btn_height = 5
    x_padding = 20
    y_padding = 20

    # 화면 크기 설정
    screen_width = 800
    screen_height = 480

    # 버튼 배치를 중앙으로 조정하기 위한 시작 좌표
    start_x = (screen_width - (btn_width * 10 * 3 + x_padding * 2)) // 2
    start_y = (screen_height - (btn_height * 2 * 3 + y_padding * 2)) // 8  # 위쪽으로 배치

    # 버튼 위치 설정
    positions = [
        (start_x, start_y), (start_x + 150, start_y), (start_x + 300, start_y),
        (start_x, start_y + 100), (start_x + 150, start_y + 100), (start_x + 300, start_y + 100),
        (start_x, start_y + 200), (start_x + 150, start_y + 200), (start_x + 300, start_y + 200)
    ]

    # 각 버튼을 생성 및 배치
    for i, symptom in enumerate(symptoms):
        x, y = positions[i]
        btn = Button(win, text=symptom, width=btn_width, height=btn_height, font=("함초롬돋움", 10), command=lambda s=symptom, u=user_inform: show_medication(s, u))
        btn.place(x=x, y=y)

    # 내비게이션 버튼 추가 (뒤로 가기 & 홈 화면)
    add_nav_buttons()

# 선택된 증상에 따라 복용해야 할 약을 추천하는 화면
def show_medication(symptom, user_inform): 
    clear_widgets()   
    history.append("medication_options")
    medication_map = {
        "소화불량": "배아제",
        "코감기": "모드콜S",
        "목감기": "모드콜S",
        "몸살": "타이레놀",
        "알러지": "알러샷",
        "두드러기": "알러샷",
        "근육통": "탁센",
        "두통": "탁센",
        "타박상": "타벡스겔"
    }
    medication = medication_map.get(symptom, None)
    if medication:
        btn = Button(win, text=medication, width=7, height=2, font=("함초롬돋움", 15), command=lambda m=medication, u=user_inform: show_medication_advice(m, u))  
        btn.place(relx=0.4, rely=0.3)  # 버튼을 중앙에 배치
    add_nav_buttons()

# 나이에 따른 약 복용법 제공
def show_medication_advice(medication, user_inform):  
    clear_widgets()                         
    history.append("medication_advice")
    advice = ""

    if user_inform[2] == "만 0~2세":     
        if medication == "타이레놀":
            advice = "증상이 약하면 복용을 삼가고, 증상이 심하면 1알을 복용하세요."
            open_close(6)
        elif medication in ["배아제", "모드콜S", "탁센", "알러샷"]:
            advice = "복용 금지"
            add_nav_buttons()
    elif user_inform[2] == "만 3~7세":
        if medication == "배아제":
            advice = "복용 금지"
            add_nav_buttons()
        elif medication == "타이레놀":
            advice = "증상이 약하면 복용을 삼가고, 증상이 심하면 1알을 복용하세요."
            open_close(6)
        elif medication == "탁센":
            advice = "증상이 약하면 1회 1알, 보통의 증상에는 1회 2알, 증상이 심하면 1회 3알씩 복용하세요."
            open_close(19)
        elif medication in ["모드콜S", "알러샷"]:
            advice = "복용 금지"
            add_nav_buttons()
    elif user_inform[2] == "만 8~12세":
        if medication == "배아제":
            advice = "1회 1알씩 복용하세요."
            open_close(13)
        elif medication == "타이레놀":
            advice = "증상이 약하면 복용을 삼가고, 증상이 심하면 1알을 복용하세요."
            open_close(6)
        elif medication == "모드콜S":
            advice = "1회 1알씩 복용하세요."
            open_close(16)
        elif medication == "탁센":
            advice = "증상이 약하면 1회 1알, 보통의 증상에는 1회 2알, 증상이 심하면 1회 3알씩 복용하세요."
            open_close(19)
        elif medication == "알러샷":
            advice = "1일 1알씩 복용하세요."
            open_close(20)
    elif user_inform[2] == "만 13~15세":
        if medication == "배아제":
            advice = "1회 1알씩 복용하세요."
            open_close(13)
        elif medication == "타이레놀":
            advice = "보통의 증상에는 1알, 증상이 심하면 2알을 복용하세요."
            open_close(6)
        elif medication == "모드콜S":
            advice = "1회 1알씩 복용하세요."
            open_close(16)
        elif medication == "탁센":
            advice = "증상이 약하면 1회 1알, 보통의 증상에는 1회 2알, 증상이 심하면 1회 3알씩 복용하세요."
            open_close(19)
        elif medication == "알러샷":
            advice = "1일 1알씩 복용하세요."
            open_close(20)
    elif user_inform[2] == "만 16세 이상":
        if medication == "배아제":
            advice = "1회 1알씩 복용하세요."
            open_close(13)
        elif medication == "타이레놀":
            advice = "보통의 증상에는 1알, 증상이 심하면 2알을 복용하세요."
            open_close(6)
        elif medication == "모드콜S":
            advice = "1회 2알씩 복용하세요."
            open_close(16)
        elif medication == "탁센":
            advice = "증상이 약하면 1회 1알, 보통의 증상에는 1회 2알, 증상이 심하면 1회 3알씩 복용하세요."
            open_close(19)
        elif medication == "알러샷":
            advice = "1일 1알씩 복용하세요."
            open_close(20)

    # 추가적인 주의사항
    if medication == "탁센":
        advice += "\n하루 5알 초과 복용 금지"
    elif medication == "모드콜S":
        advice += "\n알러샷과 동시 복용 금지"
    elif medication == "알러샷":
        advice += "\n모드콜S와 동시 복용 금지"
    elif medication == "타벡스겔":
        advice += "겔을 짜서 타박상이 있는 부위에 가볍게 발라주세요."

    label = Label(win, text=advice, font=("함초롬돋움", 15))
    label.place(relx=0.5, rely=0.3, anchor="center")



# 처방약 기능 (불완전한 코드)
# 버튼 제어 변수
prescription_set = False
morning_selected = False
lunch_selected = False
dinner_selected = False

# 처방약 첫 페이지 (아침/점심/저녁 약 등록)
def prescription_buttons():
    clear_buttons()
    history.append("prescription")

    if prescription_set:
        if morning_selected:
            label1 = Label(win, text="아침 ", font=("함초롬돋움", 15))
            label1.pack()
        if lunch_selected:
            label2 = Label(win, text="점심 ", font=("함초롬돋움", 15))
            label2.pack()
        if dinner_selected:
            label3 = Label(win, text="저녁 ", font=("함초롬돋움", 15))
            label3.pack()
        label = Label(win, text="설정 완료", font=("함초롬돋움", 15))
        label.pack()
        reset_prescription_btn = Button(win, text="처방약 해제", font=("함초롬돋움", 15), command=reset_prescription)
        reset_prescription_btn.pack()
    else:
        set_prescription_btn = Button(win, text="처방약 등록", font=("함초롬돋움", 15), command=set_prescription)
        set_prescription_btn.pack()
    add_nav_buttons()

# 처방약 세팅
def set_prescription():
    clear_buttons()
    history.append("set_prescription")
    global prescription_set
    prescription_set = False
    label = Label(win, text="처방받은 약의 복용 주기를 선택하시오", font=("함초롬돋움", 15))
    label.pack()
    def toggle_morning():
        global morning_selected
        morning_selected = not morning_selected
   
    def toggle_lunch():
        global lunch_selected
        lunch_selected = not lunch_selected
   
    def toggle_dinner():
        global dinner_selected
        dinner_selected = not dinner_selected
   
    morning_btn = Button(win, text="아침", font=("함초롬돋움", 15), command=toggle_morning)
    morning_btn.pack()
    lunch_btn = Button(win, text="점심", font=("함초롬돋움", 15), command=toggle_lunch)
    lunch_btn.pack()
    dinner_btn = Button(win, text="저녁", font=("함초롬돋움", 15), command=toggle_dinner)
    dinner_btn.pack()
    select_btn = Button(win, text="선택", font=("함초롬돋움", 18), command=prescription_setting_suceed)
    select_btn.pack()
    add_nav_buttons()

# 처방약 등록 완료를 보여줌
def prescription_setting_suceed():
    clear_buttons()
    history.append("pre_suceed")
    global prescription_set
    prescription_set = True

    label = Label(win, text="처방약 등록이 완료되었습니다.", font=("함초롬돋움", 15))
    label.pack()
    add_nav_buttons()

# 처방약 정보 초기화 확인 화면
def reset_prescription():
    clear_buttons()
    history.append("reset_prescription")
    global prescription_set
    prescription_set = True
    label = Label(win, text="처방약을 초기화하시겠습니까?", font=("함초롬돋움", 15))
    label.pack()
    yes_btn = Button(win, text="예", font=("함초롬돋움", 15), command=reset_to_prescription)
    yes_btn.pack()
    no_btn = Button(win, text="아니오", font=("함초롬돋움", 15), command=go_home)
    no_btn.pack()

# 등록된 처방약 정보 초기화
def reset_to_prescription():
    global prescription_set
    prescription_set = False
    go_home()

# 타이머 기능 추가하기 위한 현재 시각 표시 기능
def what_time():
    # Datetime
    from datetime import datetime
    print(datetime.now())

    time_btn = Button(win, text = "현재 시각", font=("함초롬돋움", 15), command=what_time)
    time_btn.pack()



# 서보모터, LED, 바코드 기능
# 홈 화면으로 돌아가기 + 문 닫힘(서보모터 off) + LED off
def ser_led_off(num):
        # GPIO 핀 번호 설정 (동일한 핀 사용)
        pin = num

        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        # 서보모터, LED 동시 제어 함수
        def control_servo_and_led():
            pwm = GPIO.PWM(pin, 50)  # PWM 객체 생성 (핀 번호, 주파수)
            pwm.start(0)  # PWM 시작, 초기 듀티 사이클 0 설정
   
            try:
            # 서보 모터 위치 조정 (같은 각도로 반복하도록) -> 0으로 바꿔줌
                pwm.ChangeDutyCycle(2.5)
                time.sleep(1)
                
            except KeyboardInterrupt:
                pwm.stop()  # PWM 정지
                GPIO.output(pin, GPIO.LOW)  # LED 초기화

        # 서보모터, LED 동시 제어 함수 호출
        try:
            control_servo_and_led()
        except KeyboardInterrupt:
            GPIO.cleanup()  # GPIO 리소스 정리

        go_home()  

# 문 열림(서보모터 on) + LED on
def ser_led(num):
        # GPIO 핀 번호 설정 (동일한 핀 사용)
        pin = num

        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        # 서보모터, LED 동시 제어 함수
        def control_servo_and_led():
            pwm = GPIO.PWM(pin, 50)  # PWM 객체 생성 (핀 번호, 주파수)
            pwm.start(0)  # PWM 시작, 초기 듀티 사이클 0 설정
   
            try:
            # 서보 모터 위치 조정 (같은 각도로 반복하도록)
                pwm.ChangeDutyCycle(7.5)
                time.sleep(1)
           
            # LED 켜기
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(1)
   
            except KeyboardInterrupt:
                pwm.stop()  # PWM 정지
                GPIO.output(pin, GPIO.LOW)  # LED 초기화

        # 서보모터, LED 동시 제어 함수 호출
        try:
            control_servo_and_led()
        except KeyboardInterrupt:
            GPIO.cleanup()  # GPIO 리소스 정리

# 서보모터와 LED on -> "처음 화면으로" 누르면 홈 화면으로 돌아가면서 서보모터와 LED off
def open_close(num):
    ser_led(num)
    serbutton=Button(win, text="처음 화면으로",  font=("함초롬돋움", 15), command=lambda: ser_led_off(num))
    serbutton.pack()

# 바코드를 통한 상품 정보 입력 화면
def check_barcode(entry):
    bar = entry.get()

    if bar == "8806723002329": # 타이레놀 6번 핀
        clear_widgets()
        label1 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label1.pack(pady=10)
        open_close(6)
       
    elif bar == "8806416004036": # 배아제 13번 핀
        clear_widgets()
        label2 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label2.pack(pady=10)
        open_close(13)

    elif bar == "8806436016712": # 탁센 19번 핀
        clear_widgets()
        label3 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label3.pack(pady=10)
        open_close(19)
       
    elif bar == "8806433062910": # 모드콜S 16번 핀
        clear_widgets()
        label4 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label4.pack(pady=10)
        open_close(16)
       
    elif bar == "8806436044814": # 알러샷 20번 핀
        clear_widgets()
        label5 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label5.pack(pady=10)
        open_close(20)
       
    elif bar == "8806422021294": # 타벡스겔  21번 핀
        clear_widgets()
        label6 = Label(win, text="문이 열렸습니다",  font=("함초롬돋움", 15))
        label6.pack(pady=10)
        open_close(21)
       
    else:
        entry.delete(0, END) # 엔트리 창 띄우기
        entry.focus()
       
    add_nav_buttons()

# 바코드로 스캔한 상품 정보를 기존에 등록된 것과 비교
def barcode_scan():
    clear_widgets()
    entry = Entry(win, font=("함초롬돋움", 20))
    entry.pack(pady=50)
    entry.focus()
    button_check = Button(win, text="확인",  font=("함초롬돋움", 15), width=10, command=lambda: check_barcode(entry))
    button_check.pack()



# 현재 화면(위젯) 정리하는 함수들
def clear_buttons():
    for widget in win.winfo_children():
        if isinstance(widget, (Button, Label, Entry, Frame)):
            widget.pack_forget()
            
def clear_widgets():
    for widget in win.winfo_children():
        widget.destroy()
        
# 뒤로 가기 버튼과 홈 버튼을 화면에 띄우는 내비게이션 함수
def add_nav_buttons():
    # 뒤로 가기 버튼
    back_btn = Button(win, text="뒤로 가기", font=("함초롬돋움", 15), command=go_back)
    back_btn.place(relx=0.6, rely=0.9)  # 아래쪽에 배치
    # 처음 화면으로 버튼
    home_btn = Button(win, text="처음 화면으로", font=("함초롬돋움", 15), command=go_home)
    home_btn.place(relx=0.4, rely=0.9)  # 아래쪽에 배치

# 홈 화면 기능
def go_home():
    clear_widgets()
    history.clear()
    show_completed_users_screen()

# 뒤로 가기 기능
def go_back(label=None):
    if label:
        label.pack_forget()
    if history:
        history.pop()  # 현재 화면을 지움
        if history:
            last_screen = history.pop()
            if last_screen == "user":
                show_user_buttons()
            elif last_screen == "gender":
                show_gender_buttons() 
            elif last_screen == "age":
                show_age_buttons()   
            elif last_screen == "confirm":
                confirm_settings()
            elif last_screen == "completed_users":
                show_completed_users_screen()
            elif last_screen == "medication":
                show_medication_buttons()   
            elif last_screen == "symptom":
                show_symptom_button()       
            elif last_screen == "symptom_options":
                show_symptom_options()      
            elif last_screen == "medication_options":
                show_medication()   
            elif last_screen == "medication_advice":
                show_medication_advice()   
            elif last_screen == "prescription":
                prescription_buttons()
            elif last_screen == "reset":
                reset_settings()


show_user_buttons()     # 초기 설정 첫 화면 띄우기
win.mainloop()          # 창을 시각화하도록 win 변수 뒤에 mainloop함수 걸어줌 (창 실행)
