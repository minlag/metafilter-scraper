import io
import time #for sleep command
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select #dropdown menus
from selenium.webdriver.support import expected_conditions as EC

# set up webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# time to rest between page loads so as not to spam
pause_time = 1

# profile of user to be scraped
url = "https://www.metafilter.com/user/20964" # lets use Shannon Larratt's as an example

# get the scraped user's id number for navigation
user_id = url.split("/")[-1] 
print("This user's ID is: ")
print(user_id)

# page where metafilter keeps all of a user's posts and comments
activity_page = "https://www.metafilter.com/activity/"


# scrape and save all posts
try:

    # go to user's activity page
    driver.get(activity_page + user_id +"/")

    # wait for end of page to finish loading
    load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )

    # find "Showing posts from:" dropdown menu and select "All Sites"
    drop_down = Select( driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/form/select') )
    drop_down.select_by_value("") # "All Sites" option is mistyped as empty in site HTML

    # get username to use as title of scraped csv
    user_name = driver.find_element(By.XPATH, '//a[@href="' + url + '"]')
    user_name = user_name.text


    # begin scraping posts in new text file
    with open(user_name + "'s_MetaFilter_Posts.csv", "w", encoding="utf-8") as file:
        
        # go to user's post activity page
        driver.get(activity_page + user_id +"/posts/1/")
            
        # write header for posts section
        print(user_name + "'s MetaFilter Posts:\n\n")
        file.write(user_name + "'s MetaFilter Posts:\n\n")
        
        # find page numbers to determine how many pages to scrape in total
        pages = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div' )
        # page numbers are always last div on this xpath
        pages = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[' + str(len(pages)) + ']' )
        # last entry is the total number of pages
        pages = pages.text.split(" ")[-1]
        print(pages, "\n\n\n")

        # pages = 1 #TESTING VARIABLE
        for page in range(1, int(pages) + 1):
            
            # go to next post activity page
            driver.get(activity_page + user_id +"/posts/" + str(page) + "/") 

            # wait for end of page to finish loading
            load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )

            #find comment titles
            # comment_title = driver.find_elements_by_class_name("posttitle")
            comment_title = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/h1')

            #find comment bodies
            # comment_body = driver.find_element_by_class_name("smallcopy postbyline")
            comment_body = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div')

            # create list of thread links by iterating through comment titles
            thread_link = []
            for index, comment in enumerate(comment_title):
                thread_link.append( comment_title[index].find_element(By.TAG_NAME, "a") )

            # write comments to file
            for index, comment in enumerate(comment_title):

                # print the thread title, comment body, and link
                print(comment_title[index].text + "\n")
                # first two entries are not comments
                print( "\t" + comment_body[index + 2].text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n")
                print( "\t\t" + thread_link[index].get_attribute('href') + "\n\n")

                # write the thread title, comment body, and link
                file.write(comment_title[index].text + "\n")
                # first two entries are not comments
                file.write( "\t" + comment_body[index + 2].text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n")
                file.write( "\t\t" + thread_link[index].get_attribute('href') + "\n\n")

                # file.write( "\t" + full_comment.text.replace("\n", "\n\t") + "\n" )

            # wait a moment to not spam
            time.sleep(pause_time)




    # begin scraping comments in new text file
    with open(user_name + "'s_MetaFilter_Comments.csv", "w", encoding="utf-8") as file:

        # go to user's post activity page
        driver.get(activity_page + user_id +"/comments/1/")

        # wait for end of page to finish loading
        load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )

        # write header for posts section
        print(user_name + "'s MetaFilter Comments:\n\n\n")
        file.write(user_name + "'s MetaFilter Comments:\n\n\n")

        # find page numbers to determine how many pages to scrape in total
        pages = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div' )
        # page numbers are always last div on this xpath
        pages = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[' + str(len(pages)) + ']' )
        # last entry is the total number of pages
        pages = pages.text.split(" ")[-1]
        print("There are " , pages , " pages to scrape\n")
        
        # store the last thread topic on a page to detect if it stretches onto the next page
        last_thread = []

        for page in range(1, int(pages) + 1):
            print("Page: ")
            print( str(page) + "\n")

             # go to next post activity page
            driver.get(activity_page + user_id +"/comments/" + str(page) + "/") 

            # wait for end of page to finish loading
            load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )

            #find comment titles
            thread_list = driver.find_elements(By.CLASS_NAME, "copy")
            # last item is not a comment
            del thread_list[-1]
            print("There are: "  ,len(thread_list),  " threads \n\n")

            # go through each thread
            for index, comment in enumerate( thread_list ):
                # refresh list of comment titles to prevent staleness 
                thread_list = driver.find_elements(By.CLASS_NAME, "copy")
                del thread_list[-1]

                # check if first thread on page is carried over from last page
                current_thread = thread_list[index].find_element(By.TAG_NAME, "a")
                print("last_thread = " + str(last_thread) + "\n")
                print("current_thread = " + current_thread.text + "\n") 
                if( str(current_thread.text) == str(last_thread) ):
                    print( "MATCH FOUND" )
                    continue

                print("link to current thread: " + str(current_thread.get_attribute('href') ) + "\n" )

                # get title of current thread
                thread_title = ( thread_list[index].find_element(By.TAG_NAME, "a").text )
                print( thread_title + "\n" )
                file.write( thread_title + "\n" )

                # list all the user's comments in the current thread 
                thread_comments = thread_list[index].find_elements( By.LINK_TEXT, user_name )
                #this for loop is a bodge to fix the "quotes within comments" issue created by identifying subcomments by "blockquote"
                for sub_index, sub_com in enumerate ( thread_comments):
                    thread_comments[sub_index] = thread_comments[ sub_index ].find_element( By.XPATH, './../..')

                # check to see if any comments in current thread have been shortened before scraping
                for short_index, short_comment in enumerate( thread_comments ):
                    more_link = thread_comments[ short_index ].find_elements( By.LINK_TEXT, "more" )
                    # always treat last thread on page as shortened to prevent missing comments continued on next page
                    if ( len( more_link ) != 0) or ( index + 1 == len(thread_list) ) :
                        shortened = True
                        break
                    else:
                        shortened = False

                # if no comments have been shortened just scrape them from current page
                if shortened == False:
                    # go through every sub comment
                    for index2, comment2 in enumerate( thread_comments ):
                        # output the sub-comment itself
                        print("\t" + thread_comments[index2].text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n" )
                        file.write("\t" + thread_comments[index2].text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n" )

                        # get sub comment's direct link
                        comment_meta = thread_comments[index2].find_elements( By.CLASS_NAME, "smallcopy" )
                        # the second item of metadata contains the comment's link
                        comment_meta = comment_meta[1].find_element( By.TAG_NAME, "a" )

                        # output the comment's direct link
                        print("\t\t" +  comment_meta.get_attribute('href') + "\n\n" )
                        file.write("\t\t" +  comment_meta.get_attribute('href') + "\n\n")

                
                # if any comment has been shortened
                else:

                        # go to the actual thread page
                        driver.get(current_thread.get_attribute('href'))

                        # wait for end of page to finish loading
                        load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )

                        # create list of all comments in the thread
                        full_comments = driver.find_elements( By.CLASS_NAME, "smallcopy" )
                        print("there are " + str(len(full_comments)) + "entries" )

                        # go through every comment on the page
                        for full_index, full_sub in  enumerate ( full_comments ):

                            # check whether a comment is by the user we are scraping
                            comment_check = full_comments[full_index].find_elements( By.LINK_TEXT, user_name )

                            #check for presence of timestamp link in comments, fixes rare edge case by stbalbach in https://www.metafilter.com/81277/The-Far-Rights-First-100-Days
                            full_link = full_comments[full_index].find_elements( By.TAG_NAME, "a")

                            #if a comment has a link to both the users profile and a timestamp it is valid for scraping
                            if ( (len(comment_check)) != 0 ) and ( (len(full_link)) == 2 ):
                                full_comment = full_comments[full_index].find_element( By.XPATH, './..')
                                # output the comment body
                                print( "\t" + full_comment.text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n" )
                                file.write( "\t" + full_comment.text.replace("\n", "\n\t").replace("posted", "\tposted") + "\n" )
                                # output the comment's direct link
                                full_link = full_comments[full_index].find_elements( By.TAG_NAME, "a")
                                print("\t\t" +  full_link[1].get_attribute('href') + "\n\n" )
                                file.write("\t\t" +  full_link[1].get_attribute('href') + "\n\n")

                        time.sleep(1)

                        driver.get(activity_page + user_id +"/comments/" + str(page) + "/") 
                        
                        # wait for end of page to finish loading
                        load_pause = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "fine-print")) )
                
                # new lines between posts for formatting
                print( "\n\n" )
                file.write( "\n\n" )

            # recreate list of comment titles to prevent staleness
            thread_list = driver.find_elements(By.CLASS_NAME, "copy")
            del thread_list[-1]
            # store the title of the last thread to detect if it stretches onto the next page
            last_thread = thread_list[-1].find_element(By.TAG_NAME, "a").text

            # regularly close webdriver instance to prevent out of memory error in chrome
            if(page % 15) == 0:
                driver.close()
                # recreate driver to prevent "invalid session id" error
                driver = webdriver.Chrome(PATH)


# quit when done scraping
finally:
    driver.quit()
    print("Scraping Finished")