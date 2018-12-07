import os
import re
import subprocess
import time

def vcodec(aim,r,name):
    os.chdir("result")
    if r == "RV20":
        if os.path.exists("RV"):
            pass
        else:
            os.mkdir("RV")
        os.chdir("RV")
        aim.append(" -c:v rv20 ")

    if r == "H263":
        if os.path.exists("H263"):
            pass
        else:
            os.mkdir("H263")
        os.chdir("H263")
        aim.append(" -c:v h263p ")

    if r == "H264":
        if os.path.exists("H264"):
            pass
        else:
            os.mkdir("H264")
        os.chdir("H264")
        aim.append(" -c:v h264 ")

    if r == "H265":
        if os.path.exists("H265"):
            pass
        else:
            os.mkdir("H265")
        os.chdir("H265")
        aim.append(" -c:v hevc ")

    if r == "JPEG":
        if os.path.exists("JPEG"):
            pass
        else:
            os.mkdir("JPEG")
        os.chdir("JPEG")
        aim.append(" -c:v mjpeg ")

    if r == "MPEG2":
        if os.path.exists("MPEG_2"):
            pass
        else:
            os.mkdir("MPEG_2")
        os.chdir("MPEG_2")
        aim.append(" -c:v mpeg2video ")

    if r == "MPEG4":
        if os.path.exists("MPEG_4"):
            pass
        else:
            os.mkdir("MPEG_4")
        os.chdir("MPEG_4")
        aim.append(" -c:v mpeg4 ")

    if r == "FLV1":
        if os.path.exists("FLV_1"):
            pass
        else:
            os.mkdir("FLV_1")
        os.chdir("FLV_1")
        aim.append(" -c:v flv1 ")

    if r == "WMV1":
        if os.path.exists("WMV_1"):
            pass
        else:
            os.mkdir("WMV_1")
        os.chdir("WMV_1")
        aim.append(" -c:v wmv1 ")

    if r == "WMV2":
        if os.path.exists("WMV_2"):
            pass
        else:
            os.mkdir("WMV_2")
        os.chdir("WMV_2")
        aim.append(" -c:v wmv2 ")

    if r == "VP8":
        if os.path.exists("VP_8"):
            pass
        else:
            os.mkdir("VP_8")
        os.chdir("VP_8")
        aim.append(" -c:v vp8 ")

    if r == "VP9":
        if os.path.exists("VP_9"):
            pass
        else:
            os.mkdir("VP_9")
        os.chdir("VP_9")
        aim.append(" -c:v vp9 ")

    return aim

def vquality(aim,r):
    q = r.split("@L")    
    aim.append(" -profile:v %s -level %s "%(q[0].lower(),q[1].lower()))
    return aim

def vsize(aim,r):
    aim.append(" -s %s "%r.lower())
    return aim

def fps(aim,r):
    rt = r.split("FPS")
    aim.append(" -r %s "%rt[0])
    return aim

def acodec(aim,r):
    if r == "AAC":
        aim.append(" -c:a aac ")
    elif r == "AC3":
        aim.append(" -c:a ac3 ")
    elif r == "MP3":
        aim.append(" -c:a mp3 ")
    elif r == "MP2":
        aim.append(" -c:a mp2 ")
    elif r == "ADPCM":
        aim.append(" -c:a adpcm_g726 ")
    elif r == "SPEEX":
        aim.append(" -c:a speex ")
    elif r == "WMA":
        aim.append(" -c:a wma2 ")
    elif r == "VORBIS":
        aim.append(" -c:a vorbis ")

    return aim

def audioBite(aim,r):
    ab = r.split("KBPS")
    aim.append(" -ab %sk "%ab[0])

    return aim

def sampling(aim,r):
    ar = r.split("KHZ")
    aim.append(" -ar %sk "%ar[0])

    return aim

def rename(pwd):
    flag = 1
    video_list = []
    path_resource =  pwd + "/resource" 
    videos = os.listdir(path_resource)
    for video in videos:
        name = video.split(".")[-1]
        os.rename(path_resource+ "/" + video,path_resource+"/V"+str(flag)+"."+name)
        flag = flag + 1

    for root, dirs, files in os.walk(path_resource):
        for file in files:            
            video_list.append(os.path.join(root, file))
            
 
    return video_list

def process_request(a):
    aim = []
    name = ""
    rs = a.split("_")
    for r in rs:
        r = r.upper()
        if re.match("H26",r) or re.match("RV20",r) or re.match("PEG",r) or re.match("FLV1",r) or re.match("WMV",r) or re.match("VP",r) :
            aim = vcodec(aim,r,name)

        elif re.match("HIGH",r) or re.match("MAIN",r) or re.match("BASELINE",r):
            aim = vquality(aim,r)

        elif re.match(r'\d+X\d+', r):
            aim = vsize(aim,r)

        elif re.match(r'\d+FPS', r):
            aim = fps(aim,r)

        elif re.match('AAC', r) or re.match("AC3",r) or re.match("ADPCM",r) or re.match("SPEEX",r) or re.match("RV20",r) or re.match("MP",r) or re.match("WMA",r) or re.match("VORBIS",r):
            aim = acodec(aim,r)

        elif re.match(r"\d+KBPS",r):
            aim = audioBite(aim,r)

        elif re.match(r"\d+KHZ",r):
            aim = sampling(aim,r)

    return aim


def run(rqs,d,i,j,err_num):
    pwd = os.getcwd()
    source_pwd = pwd
    video_list = rename(pwd)
    aim = process_request(rqs)
    num  = len(video_list)    
    for video in video_list:
        j += 1
        cmd = ""
        cmd_all = "ffmpeg -i "
        for item in aim:
            cmd = cmd + item
        
        name = video.split("/")[-1].split(".")[0]
        cmd_all = cmd_all + video + cmd + "-strict -2 " + os.getcwd() + "/" + name + "_" + rqs
        flag_video = os.system(cmd_all)
        print("*"*80)
        
        if flag_video == 0:
            print("*"*80)
            print("\t完成视频文件 %s 的转换"%video)
            i += 1
            print("\t任务进度  ----------  %s/%s"%(str(i), str(num*d)))
            print("*"*80)
        else:
            cmd_th = j//num + 1
            video_th = j%num
            all_th = str(cmd_th) + " " + str(video_th)
            err_num.append(all_th)
            print("*"*80)
            print("\t请检查要求的文件格式或源文件是否有误！")
            print("\t任务进度  ----------  %s/%s"%(str(i), str(num*d)))
            print("*"*80)
        #os.system(cmd_all)
        time.sleep(2)
    if source_pwd == os.getcwd():
        pass
    else:
        os.chdir("../..")
    print(os.getcwd())
    return i,j,err_num,num




    

    

def main():
    if os.path.exists("result"):
        pass
    else:
        os.mkdir("result")

    f = open("request.txt", "r")
    d = 0
    i = 0
    j = 0
    err_num = []
    request_lists = f.readlines()
    for request in request_lists:
        if request.strip() == "":
            pass
        else:
            d = d+1
    for request in request_lists:
        if request.strip() == "":
            pass
        else:
            (i,j,err_num,num) = run(request.strip(),d,i,j,err_num)
    if i == num*d:
        pass
    else:
        print("\t失败的是：")
        for item in err_num:
            cmd_th = item.split(" ")[0]
            video_th = item.split(" ")[1]
            if video_th == "0":
                cmd_th = str(int(cmd_th)-1)
                video_th = num
            print("\t第%s条命令的第%s个视频"%(cmd_th,video_th))

if __name__ == "__main__":
    main()

