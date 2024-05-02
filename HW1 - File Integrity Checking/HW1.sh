#!/bin/bash
function error1_check() { #예외처리1 : 매개변수 작성 안했을 경우
    if [ -z "$1" ] 
    then
        echo "Usuage: $2 [directory]"
        exit 0
    fi
}

function error2_check() { #예외처리2 : config 파일이 존재하지 않을 경우
    if [ ! -e "config" ] 
    then
        echo "Config does not exist."
        exit 0
    fi
}

function error3_check() { #예외처리3 : 매개변수로 받은 directory나 파일이 존재하지 않을 경우
    if [ ! -e "$1" ] 
    then
        echo "$1 does not exist."
        exit 0
    fi
}

function relative_check() { #상대경로인지 아닌지 체크하고 절대경로로 바꿔준다
    if [[ $1 == /* ]] #/로 시작하면 절대경로이므로 그냥 return
    then
        path="$1"
    else #아니면 상대경로이므로 절대경로로 바꿔서 return
        path="$(realpath "$1")"
    fi
    echo "$path"
}

function dir_check() { #config내 hash.txt파일의 경로가 없다면 만들어준다.
    if [ "$1" == "" ] #config내 경로가 비어있다면 현재 디렉터리에 생성하도록 현재 경로로 설정해준다.
    then
        path=$(pwd)
    else
        path=$1
        path=${path%/hash.txt} #경로 존재 여부 확인을 위해 뒤에 /hash.txt 적힌 부분을 없애준다.
        if [ ! -d "$path" ]
        then
            mkdir -p "$path"
        fi
        path=$(relative_check $path) #config에 상대경로가 적혀있을 수 있으므로 절대경로로 변환
    fi
    echo "$path/hash.txt" #다시 원래 hash.txt 경로로 return
}

function get_list() { #hash.txt에 있는 값들을 load
    tmp=""
    if [ -e "$1" ] #이미 hash.txt가 있다면 불러온다
    then
        tmp=$(cat "$1")
    fi
    echo "$tmp"
}

#main
error1_check "$1" "$0"
error2_check
error3_check $1
read -r tmp < "config" #hash.txt 경로를 config에서 불러오기
hash_path=$(dir_check $tmp)
trace_path=$(relative_check $1)
list=$(get_list $hash_path)
new="" #새로운 해시값들을 임시로 담을 곳
while read -r -d '' line <&3; #매개변수로 받은 경로의 모든 파일들을 찾아서 경로를 한줄씩 읽어온다.
do
    hash=$(sha1sum "$line" | awk '{print $1}')
    path=$(sha1sum "$line" | awk '{print $2}')
    if ! echo "$list" | grep -w -q "$path" #경로가 존재하지 않을 때만 새로 추가
    then
        echo -e "\n[NEW] $path ($hash)"
        new="$new$hash $path\n"
    else
        old_hash=$(echo "$list" | grep -w "$path" | awk '{print $1}') #path로 hash.txt에서 행을 찾고 $1(기존 hash)값을 반환
        flag=$(echo "$list" | grep -w "$hash $path" | awk '{print $1}') #이번엔 hash까지 묶어서 grep -> 변화가 있으면 flag는 NULL값이다.
        if [ "$flag" == "" ] #변화가 있을 경우 warn 출력
        then
            echo -e "\n[WARN] $path \n(old: $old_hash, new: $hash)"
            echo -e "\n================================================================================"
            echo -e "\n$path is changed."
            echo -e "\nDo you want to update the hash of $path (y|n)?"
            read opt
            if [ "$opt" == "y" ] #선택이 y면 해시값을 업데이트
            then
                list=$(echo "$list" | sed -e "s|.*$path|$hash $path|") #sed로 old_hash부분을 tmp_hash로 변경
                echo -e "\ny : Change hash value"
            elif [ "$opt" == "n" ]
            then
                echo -e "\nn : No change"
            else
                echo -e "\nWrong option"
            fi
            echo -e "\n================================================================================"
        fi
    fi
done 3< <(find "$trace_path" -type f -print0)
list="$list$new" #새롭게 추가한 해쉬값을 추가
echo -e "\nIntegrity check completed.\n"
echo -e "$list" > "$hash_path" #hash.txt로 변환해서 hash.txt에 저장
exit 0