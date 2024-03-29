# -*- coding: utf-8 -*-

from selenium       import webdriver
from urllib.request import urlretrieve
from time           import sleep
from datetime       import datetime
from turtle_log     import Log
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os
import re

class PostStats:
    post_count  = 0
    image_count = 0
    video_count = 0

class Driver:
    PHANTOM = 1
    CHROME  = 2
    FIREFOX = 3

class Download_Choice:
    DOWNLOAD_ALL    = 1
    UPDATE          = 2
    SOME            = 3

stats = {}
followers_count = 0
following_count = 0

class Turtle:

    _pic_path        = "pictures"
    _driver          = None
    log              = None

    _pic_user_path      = ""
    _pic_user_vid_path  = ""

    file = ""
    post_history = ""

    _start = ""
    _end   = ""

    imgLinks    = []

    _status_driver  = False
    _status_sign_in = False
    _status_links   = False
    result          = False

    # Set Path (optional) | return : None
    def set_path(self, path):
        self._pic_path = path

    # Set Start (optional) | return : None
    def set_start(self, start):
        self._start = start 

    # Set End (optional) | return : None
    def set_end(self, end):
        self._end = end 

    # Set Driver | return : True
    def _set_driver(self, driver_choice):
        if driver_choice == Driver.CHROME:
            self._driver = webdriver.Chrome()
        elif driver_choice == Driver.FIREFOX:
            self._driver = webdriver.Firefox()
        else:
            self._driver = webdriver.PhantomJS()
        return True

    # Open driver and Log | return : True or False
    def open(self, driver_choice = Driver.PHANTOM):
        try:
            self._set_driver(driver_choice)
            date = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
            self.log = Log(date)
            
            self.log.append("PROGRAM STARTED!", False)
            driver_name = next(name for name, value in vars(Driver).items() if value == driver_choice)
            self.log.append("Driver : " + str(driver_name), False)

            self._status_driver = True
            return True
        except Exception as exp:
            self.log.append_exception(exp)
            self._status_driver = False
            return False

    # Close driver and remove cookies | return : True or False
    def close(self):
        try:
            self._driver.delete_all_cookies()
            self._driver.quit()
            self.log.append("Browser closed successfuly.")
            return True
        except Exception as exp:
            self.log.append_exception(exp)
            return False

    # Sign in to Instagram | return : True or False
    def sign_in(self, username, password):
        if not self._status_driver:
            self._status_sign_in = False            
            return False
        try:
            self._driver.get("https://www.instagram.com/accounts/login")
            sleep(2)
            
            # Send user info
            self._driver.find_element_by_name("username").send_keys(username)
            self._driver.find_element_by_name("password").send_keys(password)
            self._driver.find_element_by_css_selector("button[type='submit']").click()   
            sleep(6)

            # If there is 2 factor verification
            try:
                self._driver.find_element_by_name("verificationCode")
                self.log.append("Username and Password are correct.")
                self.log.append("## (INFO) Verification Found!")

                # Verification Code
                for i in range(5):
                    try :
                        code = input("The code, sent to your phone by Instagram : ")
                        print("lvl1")
                        self._driver.find_element_by_name("verificationCode").clear()
                        print("lvl2")
                        self._driver.find_element_by_name("verificationCode").send_keys(code)
                        print("lvl3")
                        self._driver.find_element_by_css_selector("button[type='button']").click()
                        print("lvl4")
                        
                        sleep(7)
                        self._driver.find_element_by_css_selector("a[href='/explore/']")
                        self.log.append("Username and Password are correct.")
                        self._status_sign_in = True    
                        return True
                    except :
                        self.log.append("Verification Error!")
                
                self.log.append("## (ERROR) Exit verification cycle.")
                self._status_sign_in = False
                return False
            except:
                pass
            
            try:
                self._driver.find_element_by_css_selector("a[href='/explore/']")
                self.log.append("Username and Password are correct.")
                self._status_sign_in = True                
                return True
            except:
                pass
        
            self.log.append("## (ERROR) Username or Password are NOT CORRECT!")
            self._status_sign_in = False
            return False
        except Exception as exp:
            self.log.append_exception(exp)
            self._status_sign_in = False
            return False

    # Get pic_user picture links | return : True or False
    def get_img_links(self, pic_user):
        if not self._status_sign_in:
            self._status_links = False
            return False
        try:
            if not pic_user:
                self.log.append("## (ERROR) Username must be given for finding photos!")
                self._status_links = False
                return False
            
            self.log.append("$ USER : " + pic_user)
            self.log.append("Getting user...")
            self._driver.get("https://www.instagram.com/" + pic_user)

            follower = self._driver.find_element_by_class_name("-nal3")
            follower = self._driver.find_element_by_class_name("-nal3")
            follower_count = follower.find_element_by_css_selector('span').get_attribute("textContent")
            print(follower_count)

            self.log.append("Listing stories...")
            
            photo_total = int(self._driver.find_element_by_class_name("g47SY").text.replace(".", "").replace(",",""))
            imgLinks = []
            count = 0
            error = 0

            while len(imgLinks) != photo_total and len(imgLinks) < 300:
                # Find all photos of current page
                imgList = self._driver.find_elements_by_css_selector(".v1Nh3 a")
                
                # Add the photos to list if not exists
                for idx, img in enumerate(imgList):
                    _link = img.get_property("href")
                    if not _link in imgLinks:
                        imgLinks.append(_link)
                
                # Write current link count to log
                if len(imgLinks) % 10 != count:
                    count = len(imgLinks) % 10
                    self.log.append(str(len(imgLinks)) + " photos found.")
                else:
                    # This means collection is not working!
                    error += 1

                # If program stops  to collect links> then break while
                if error == 10:
                    self.log.append("## (ERROR) Circle broken for user : " + pic_user)
                    self._status_links = False
                    return False
                
                # Scroll down the picture
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

            self.log.append("> " + str(len(imgLinks)) + " < links found.")
            self.imgLinks = imgLinks

            self._status_links = True
            return True
        except Exception as exp:
            self.log.append_exception(exp)
            self._status_links = False
            return False

    # Create user folders and set to self. | return : True or False
    def _create_pic_user_folders(self, pic_user, create_video_dir = True):
        try:
            # User root folder
            path = self._pic_path + "/" + pic_user

            if not os.path.exists(path):
                os.makedirs(path)
            self._pic_user_path = path

            # User pic folder
            if create_video_dir:
                vid_path = path + "/" + "videos"

                if not os.path.exists(vid_path):
                    os.makedirs(vid_path)
                self._pic_user_vid_path = vid_path


            self.file = open( path + "_index.html", "w+" )
            self.post_history = open( path + "_post_history.csv", "w+" )
            self.file.write("<!DOCTYPE html>\n")
            self.file.write("<html>\n")
            self.file.write("<head>\n")
            self.file.write("<style>\n")
            self.file.write("div.gallery {\n")
            self.file.write("  margin: 5px;\n")
            self.file.write("  border: 1px solid #ccc;\n")
            self.file.write("  float: left;\n")
            self.file.write("  width: 320px\n")
            self.file.write("}\n")
            self.file.write("\ndiv.gallery img {\n")
            self.file.write("  width: 100%;\n")
            self.file.write("  heightL auto;\n")
            self.file.write("}\n\n")
            self.file.write("div.desc {\n")
            self.file.write("  padding: 15px\n")
            self.file.write("  text-align: center;\n")
            self.file.write("}\n")
            self.file.write("</style>\n")
            self.file.write("</head>\n")
            self.file.write("<body>\n")
            self.file.write("<div>\n")
            self.file.write("<h1>")
            userstr = "@" + pic_user
            self.file.write(userstr)
            self.file.write("</h1>\n")
            self.file.write("<h2>\n")
            timestr = self._start + " - " + self._end;
            self.file.write(timestr)
            self.file.write("</h2>\n")
            self.file.write('<a href="' + pic_user + '_post_history.csv'+ '">Post History CSV File</a>')
            self.file.write("</div><br>\n")

            return True;

        except Exception as exp:
            self.log.append_exception(exp)
            return False
    
    def get_comments( self, path, pic_user ):

        self._driver.get(path) #go to first picture
        p = re.split("[/]",path)
        comment_str = p[-2]
        comment_file_path = 'pictures/' + pic_user + '/' + comment_str + '.html'
        f = open( comment_file_path, "w+")

        f.write('<meta charset="UTF-8">')

        # approximately 12 comments per page
        click_count=0

        while (1):
            try:
                load_more = self._driver.find_element_by_class_name("glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
                actions.move_to_element(load_more).perform()
                load_more.click()
                click_count+=1
                time.sleep(2)
            except Exception as e:
                print(e)
                break
        
        print("final click count: " + str(click_count) + "; should yield roughly " + str(click_count*12) + " comments")

        comments = self._driver.find_elements_by_class_name("C4VMK")
    
        comments_list, users_list = [], []
    
        for c in comments:
            comment = c.find_element_by_css_selector('span').get_attribute("textContent")

            if comment == "Verified":
                comment = c.find_element_by_css_selector('span:nth-child(2)').get_attribute("textContent")

            user = c.find_element_by_class_name("TlrDj").get_attribute("textContent")
            comment_text = '<p>@' + user + ": " + str(comment) + '</p> <br>'


            f.write( comment_text )

            comments_list.append(comment)
            users_list.append(user)
    
            df = pd.DataFrame({"user": users_list, "comment": comments_list})
            
            df.to_csv("instagram_comments.csv", index=False)

    
        f.close()
 
    # Download all pictures | return : 0 or Total_Downloaded_Photo_Number
    def download_photos(self, pic_user_folder_name, download_choice = Download_Choice.UPDATE, download_photo_number = 0, download_video = True):
        if not self._status_links:
            self.result = False
            return 0
        try:
            total_photo_number      = len(self.imgLinks)
            download_number         = 0
            already_exists_number   = 0
            just_last_photos        = True
            total_download          = 0
            done                    = False

            # Set Download Choice
            if download_choice == Download_Choice.UPDATE:
                total_download = total_photo_number
                just_last_photos = True

            elif download_choice == Download_Choice.SOME and download_photo_number > 0:
                total_download = download_photo_number
                just_last_photos = False
            
            elif download_choice == Download_Choice.SOME and download_photo_number <= 0:
                raise Exception("Download photo number must be bigger than 0!")

            elif download_choice == Download_Choice.DOWNLOAD_ALL:
                total_download = total_photo_number
                just_last_photos = False

            else:
                raise Exception("Invalid download choice!")

            # Create pic_user folders
            self._create_pic_user_folders(pic_user_folder_name, download_video)

            # Download Photos
            for idx, link in enumerate(self.imgLinks):

                # Go To Link
                self._driver.get(link)


                # Get Photo Taken Date
                post_date = self._driver.find_element_by_tag_name("time").get_attribute("datetime").split("T")[0]; 
                print( post_date );
                post_datetime = datetime.strptime( post_date, '%Y-%m-%d')
                start_datetime = datetime.strptime( self._start, '%Y-%m-%d')
                time = self._driver.find_element_by_tag_name("time").get_attribute("datetime").split("T")[0] + "_"
                end_datetime = datetime.strptime( self._end, '%Y-%m-%d')

                
                # if we've gone far enough back then stop 
                if post_datetime < start_datetime: break 

                # if we've not gone far enough then skip it
                if post_datetime > end_datetime: continue

                # Start stat collection
                if post_datetime not in stats:
                   stats[post_datetime] = PostStats()
                   print ( 'Added' )
                   print ( post_datetime )
                
                stats[post_datetime].post_count = stats[post_datetime].post_count + 1
                # If page has many photos
                try:
                    img_count = self._driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges.length')
                    for i in range(img_count):
                        is_video = self._driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.is_video')
                        
                        if is_video:   
                            # Video check
                            if not download_video: continue

                            img_link = self._driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.video_url')
                            stats[post_datetime].video_count = stats[post_datetime].video_count + 1
                        else:
                            img_link = self._driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.display_url')
                            stats[post_datetime].image_count = stats[post_datetime].image_count + 1
                        
                        # Create Name
                        s = img_link.split("/")
                        name = time + s[-1].split("?")[0]

                        # Download photos
                        if is_video:    
                            path = self._pic_user_vid_path + "/" + name
                        else:           
                            path = self._pic_user_path + "/" + name
                        
                        if not os.path.isfile(path):
                            urlretrieve(img_link, path)
                            download_number += 1
                        else:
                            if just_last_photos:
                                done = True
                            already_exists_number += 1

                        post_date = self._driver.find_element_by_tag_name("time").get_attribute("datetime").split("T")[0]; 
                        post_datetime = datetime.strptime( post_date, '%Y-%m-%d')
                        date_string = post_datetime.strftime('%b %d %Y')
    
                        self.file.write("<div class=""gallery"">\n")
    
                        if is_video:
                            videostr = '<video width="320" height="320" controls>'
                            self.file.write(videostr)
                            videostr = '<source src="../' + path + '" type="video/mp4">'
                            self.file.write(videostr)
                            self.file.write('</video>')
                        else:
                            filestr = '<a target="_blank" href=\"' + '../' + path + '">\n'
                            self.file.write(filestr)
                            filestr = ' <img src="' + '../' + path + '"alt="'+time+'" width="320" height="320">\n'
                            self.file.write(filestr)
                            self.file.write("   </a>\n")

                        p = re.split("[/]",link)
                        comment_str = p[-2]
    
                        comment_str = '<div class="desc"><a href="' +pic_user_folder_name+ '/'+ comment_str +  '.html' + '">' + date_string + ': Caption and Comments</a></div>\n'
                        self.file.write(comment_str)
    
                        likes = self._driver.find_elements_by_class_name("Nm9Fw")
                        for l in likes:
                            likes_span = l.find_element_by_css_selector('span').get_attribute("textContent")
                            print(likes_span)

                            likes_str = '<div class="desc">'+'<b>MultiPic</b> Post Likes: '+ likes_span +'</div>\n'
                            self.file.write(likes_str)

                        self.file.write("</div>\n")

                        self.get_comments(link, pic_user_folder_name)

                        #stats[post_datetime].post_count = stats[post_datetime].post_count + 1

                # If page has single photo
                except:
                    try:
                        # If it is a video
                        img_link = self._driver.find_element_by_tag_name("video").get_attribute("src")
                        is_video = True
                        print("Found a video\n");
                        # Video Download allowed check
                        if not download_video: continue
                    except:
                        print("Found an image\n");
                        # Get Picture URL
                        tag = self._driver.find_element_by_css_selector('meta[property="og:image"]')
                        img_link = tag.get_property("content")
                        is_video = False
                    
                    # Create Name
                    s = img_link.split("/")
                    name = time + s[-1].split("?")[0]
                    
                    # Download photos
                    if is_video:    path = self._pic_user_vid_path + "/" + name
                    else:           path = self._pic_user_path + "/" + name
                    
                    if not os.path.isfile(path):
                        urlretrieve(img_link, path)
                        download_number += 1

               
                    else:
                        if just_last_photos: done = True
                        already_exists_number += 1
                
                    post_date = self._driver.find_element_by_tag_name("time").get_attribute("datetime").split("T")[0]; 
                    post_datetime = datetime.strptime( post_date, '%Y-%m-%d')
                    date_string = post_datetime.strftime('%b %d %Y')

                    self.file.write("<div class=""gallery"">\n")

                    if is_video:
                        videostr = '<video width="320" height="320" controls>'
                        self.file.write(videostr)
                        videostr = '<source src="../' + path + '" type="video/mp4">'
                        self.file.write(videostr)
                        self.file.write('</video>')
                        stats[post_datetime].video_count = stats[post_datetime].video_count + 1
                    else:
                        filestr = '<a target="_blank" href=\"' + '../' + path + '">\n'
                        self.file.write(filestr)
                        filestr = ' <img src="' + '../' + path + '"alt="'+time+'" width="320" height="320">\n'
                        self.file.write(filestr)
                        self.file.write("   </a>\n")
                        stats[post_datetime].image_count = stats[post_datetime].image_count + 1

                    p = re.split("[/]",link)
                    comment_str = p[-2]

                    comment_str = '<div class="desc"><a href="' +pic_user_folder_name+ '/'+ comment_str +  '.html' + '">' + date_string + ': Caption and Comments</a></div>\n'
                    self.file.write(comment_str)

                    likes = self._driver.find_elements_by_class_name("Nm9Fw")
                    for l in likes:
                        likes_span = l.find_element_by_css_selector('span').get_attribute("textContent")

                        likes_str = '<div class="desc">'+'Likes: '+ likes_span +'</div>\n'
                        self.file.write(likes_str)

                    self.file.write("</div>\n")

                    self.get_comments(link, pic_user_folder_name)

                # Info
                self.log.append("> " + str(idx + 1) + " / " + str(total_download) + " stories downloaded...")
                    
                # Max photo check - Break outer loop when inner loop broken
                if idx == total_download - 1 or done:
                    self.log.append("> " + str(idx + 1) + " < stories downloaded.")
                    break

            # Log information
            self.log.append("-------------------------------")
            self.log.append("$ Download Completed.")
            self.log.append("$ Total user stories      : " + str(total_photo_number))
            self.log.append("$ Total harvested stories : " + str(total_download))
            self.log.append("$ Total harvested photos  : " + str(download_number + already_exists_number))
            self.log.append("$ Total Download          : $ " + str(download_number) + " $")
            self.log.append("$ Already exists          : " + str(already_exists_number))
            self.log.append("-------------------------------")

            self.file.write("<!DOCTYPE html>")
            self.file.write("<html>")
            self.file.write("<head>")
            self.file.write("<style>")
            self.file.write("table {")
            self.file.write("font-family: arial, sans-serif;")
            self.file.write("border-collapse: collapse;")
            self.file.write("width: 100%;")
            self.file.write("}")
            self.file.write("")
            self.file.write("td, th {")
            self.file.write("border: 1px solid #dddddd;")
            self.file.write("text-align: left;")
            self.file.write("padding: 8px;")
            self.file.write("}")
            self.file.write("")
            self.file.write("tr:nth-child(even) {")
            self.file.write("background-color: #dddddd;")
            self.file.write("}")
            self.file.write("</style>")
            self.file.write("</head>")
            self.file.write("<body>")

            self.file.write("<table>")
            self.file.write("<tr>")
            self.file.write("<th>Date</th>")
            self.file.write("<th>Post Count</th>")
            self.file.write("<th>Image Count</th>")
            self.file.write("<th>Video Count</th>")
            self.file.write("</tr>")

            # september 3rd is the 246th day
            for day in range(3, 247):
               self.post_history.write(',')
               daystr = datetime.fromordinal(day)
               daystr = daystr.replace( year=2019 )
               self.post_history.write(daystr.strftime('%Y-%m-%d'))

            self.post_history.write('\n')
            self.post_history.write(pic_user_folder_name)
                
            for day in range(3, 247):
               self.post_history.write(',')
               daystr = datetime.fromordinal(day)
               daystr = daystr.replace( year=2019 )
               keystr = daystr.strftime('%Y-%m-%d')
               value = stats.get(daystr)
               if not value:
                  self.post_history.write('0')
                  print(keystr)
               else:
                  self.post_history.write( str( stats[daystr].post_count ) )
              

             
            for key, value in stats.items():
              post_datetime = key.strftime('%Y-%m-%d')
              print(post_datetime, value.post_count, value.image_count, value.video_count )
              self.file.write("<tr>")
              tablestr = '<td>' + post_datetime + '</td>'
              self.file.write(tablestr)
              tablestr = '<td>' + str(value.post_count) + '</td>'
              self.file.write(tablestr)
              tablestr = '<td>' + str(value.image_count) + '</td>'
              self.file.write(tablestr)
              tablestr = '<td>' + str(value.video_count) + '</td>'
              self.file.write(tablestr)
              self.file.write("</tr>")


            self.file.close()
            self.post_history.close();
            
            self.result = True

            return download_number
        except Exception as exp:
            self.log.append_exception(exp)
            self.result = False
            return 0



class Turtle_Quick:

    @staticmethod
    def download_all_user_pic(username, password, pic_user, path = None, driver = Driver.PHANTOM):
        t = Turtle()
        if path:
            t.set_path(path)
        t.open(driver)
        t.sign_in(username, password)
        t.get_img_links(pic_user)
        t.download_photos(pic_user, Download_Choice.DOWNLOAD_ALL)
        t.close()
        del(t)

    @staticmethod
    def update_user_pic(username, password, pic_user, path = None, driver = Driver.PHANTOM):
        t = Turtle()
        if path:
            t.set_path(path)
        t.open(driver)
        t.sign_in(username, password)
        t.get_img_links(pic_user)
        t.download_photos(pic_user, Download_Choice.UPDATE)
        t.close()
        del(t)

    @staticmethod
    def download_some_user_pic(username, password, pic_user, count, path = None, driver = Driver.PHANTOM):
        t = Turtle()
        if path:
            t.set_path(path)
        t.open(driver)
        t.sign_in(username, password)
        t.get_img_links(pic_user)
        t.download_photos(pic_user, Download_Choice.SOME, count)
        t.close()
        del(t)
