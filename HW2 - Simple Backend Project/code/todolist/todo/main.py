import requests

print("\n********************** Todo-list API Test **********************")
while True:
    url = "http://127.0.0.1:8000/tasks/" #end-point url
    print("\n========================= Test Option =========================")
    print("0 : Add new task              | 1 : Load all tasks")
    print("2 : Load completed tasks      | 3 : Load not completed tasks")
    print("4 : Load 1st prior rank tasks | 5 : Change task completion")
    print("6 : Modify task content       | 7 : Delete specific task")
    print("8 : Delete completed tasks    | 9 : Delete all tasks")
    print("Other input : Termination\n")
    n = input("Select API test you want >> ")
    print("\n======================== Test Progress ========================")
    match n:
        case '0':
            url += "create/"
            test_content = input("Enter content >> ")  #내용 입력하기
            test_date = input("Enter Date (yyyy-mm-dd) >> ")  #날짜 입력하기, 오입력 예외처리는 구현X
            test_prior = int(input("Enter Priority : 1(High), 2(Mid), 3(Low) >> "))  #우선순위 입력하기 (1~3), 오입력 예외처리는 구현X
            data = {"content": test_content, "due_date": test_date, "completed": False, "prior_rank": test_prior} #completed는 False가 기본값
            response = requests.post(url, json=data) #POST
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력 (post는 status가 201)
                print(response.text)
            else:
                print(f"Error {response.status_code}: Test failed")
        case '1':
            url += "list/"
            response = requests.get(url) #GET
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                print("To-do list:")
                for i in response.json():
                    print(i)
            else:
                print(f"Error {response.status_code}: Test failed")
        case '2':
            url += "completed/"
            response = requests.get(url)
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                print("Completed to-do list:")
                for i in response.json():
                    print(i)
            else:
                print(f"Error {response.status_code}: Test failed")
        case '3':
            url += "incompleted/"
            response = requests.get(url)
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                print("No completed to-do list:")
                for i in response.json():
                    print(i)
            else:
                print(f"Error {response.status_code}: Test failed")
        case '4':
            url += "high-prior/"
            response = requests.get(url)
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                print("Important to-do list:")
                for i in response.json():
                    print(i)
            else:
                print(f"Error {response.status_code}: Test failed")
        case '5':
            test_id = int(input("Input ID of completed task >> "))  #완료로 변경하고자 하는 할일의 ID
            url += str(test_id) + "/"
            response = requests.get(url)
            if response.status_code == 200: #id가 존재할때만 진행
                url += "complete/"
                response = requests.patch(url)
                if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                    print(f"Change task(id={test_id}) to completed.")
                else:
                    print(f"Error {response.status_code}: Test failed")
            else:
                print(f"Error {response.status_code}: Test failed")
        case '6':
            test_id = int(input("Input ID you want to motify >> "))  #수정하고자 하는 할일의 ID
            url += str(test_id) + "/"
            response = requests.get(url)
            if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                print("Current todo:", response.json())
                flag = input("Do you want to modify this? (y/n) >> ") #완료 여부 선택, 일단 y 이외의 답은 n로 간주 (예외처리 구현X)
                if (flag == 'y'):
                    test_content = input("Content >> ")  #내용 수정하기
                    test_date = input("Date (yyyy-mm-dd) >> ")  #날짜 수정하기, 오입력 예외처리는 구현X
                    test_com = input("Completion (y/n) >> ") #완료 여부 선택, 오입력 예외처리는 구현X
                    test_com = True if test_com == 'y' else False
                    test_prior = int(input("Priority : 1(High), 2(Mid), 3(Low) >> "))  #우선순위 수정하기 (1~3), 오입력 예외처리는 구현X
                    data = {"content": test_content, "due_date": test_date, "completed": test_com, "prior_rank": test_prior}
                    url += "modify/"
                    response = requests.put(url, data=data)
                    if response.status_code == 200: #에러가 없을 때만 JSON 파싱 후 출력
                        print("After todo:", response.json())
                    else:
                        print(f"Error {response.status_code}: Test failed")
            else:
                print(f"Error {response.status_code}: Test failed")
        case '7':
            test_id = int(input("Input ID you want to delete >> "))  #삭제하고자 하는 할일의 ID
            url += str(test_id) + "/delete/"
            response = requests.delete(url)
            if response.status_code == 204: #에러가 없을 때만 JSON 파싱 후 출력 (delete는 status가 204)
                print(f"Delete task(id={test_id}).")
            else:
                print(f"Error {response.status_code}: Test failed")
        case '8':
            url += "delete-completed/"
            response = requests.delete(url)
            if response.status_code == 204: #에러가 없을 때만 JSON 파싱 후 출력 (delete는 status가 204)
                print(f"Delete all completed tasks.")
            else:
                print(f"Error {response.status_code}: Test failed")
        case '9':
            url += "delete-all/"
            response = requests.delete(url)
            if response.status_code == 204: #에러가 없을 때만 JSON 파싱 후 출력 (delete는 status가 204)
                print(f"Delete all tasks.")
            else:
                print(f"Error {response.status_code}: Test failed")
        case _:
            print("Test is over.")
            print("\n************************** TERMINATE **************************")
            exit(0)