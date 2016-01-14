import urllib.request
import json
import re


def get_graph_url(graph_url, app_id, app_secret):
    post_args = "/feed/?key=value&access_token=" + app_id + "|" + app_secret
    post_url = graph_url + post_args
    return post_url


def get_comments_url(graph_url, app_id, app_secret):
    post_args = "/comments/?key=value&access_token=" + app_id + "|" + app_secret
    post_url = graph_url + post_args
    return post_url


def get_json_response(post_url):
    web_response = urllib.request.urlopen(post_url)
    readable_page = web_response.read().decode("utf-8")
    json_post_data = json.loads(readable_page)
    return json_post_data


def write_posts_to_a_file(json_fb_posts, maximum_posts, starting_post_no):
    regex_for_number = r'([0-9]+)'
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    f = open('posts.txt', 'a', encoding='utf-8')
    for i, post in enumerate(json_fb_posts):
        print("Processing Post No: %s" % str(i + 1 + starting_post_no))
        if 'message' in post.keys():
            post['message'] = post['message'].replace("\n",' ')
            comment_id = post['id']
            app_id = '416379438547915'
            app_secret = 'e1c66cb8409855dcf19bf01cb8bdcd6a'
            graph_url = "https://graph.facebook.com/" + str(comment_id)
            comment_url = get_comments_url(graph_url, app_id, app_secret)
            json_post_data = get_json_response(comment_url)
            comments = json_post_data['data']
            while 'paging' in json_post_data.keys() and 'next' in json_post_data['paging'].keys():
                print(" ----- Downloading Comments ----- ")
                post_url = json_post_data['paging']['next']
                json_post_data = get_json_response(post_url)
                comments.extend(json_post_data['data'])

            for j, comment in enumerate(comments):
                print("---- Processing Comment No %s of Post No %s ----" % (str(j + 1), str(i + 1 + starting_post_no)))
                if 'message' in comment.keys():
                    comment_message = comment['message']
                    comment_person_name = comment['from']['name']
                    numbers = []
                    email_matches = []
                    final_number = ""
                    final_email = ""
                    try:
                        numbers = re.findall(regex_for_number, comment['message'], re.I)
                    except:
                        print(" No Number Found")
                    try:
                        email_matches = regex.findall(comment['message'])
                    except:
                        print(" No Email Found")

                    for number in numbers:
                        if len(number) >= 10:
                            final_number = number
                            break

                    for email in email_matches:
                        final_email = email[0]
                        break

                    if len(final_email) >= 5 or len(final_number) >= 5:

                        f.write("-----------------------------*********************----------------------------")
                        f.write("\n")
                        f.write("\n")
                        f.write("------ CORRESPONDING POST -----")
                        f.write("\n")
                        f.write(str(post['message']))
                        f.write("\n")
                        f.write("------ CORRESPONDING COMMENT -----")
                        f.write("\n")
                        f.write(str(comment_message))
                        f.write("\n")
                        f.write("------ CORRESPONDING NAME OF THE PERSON -----")
                        f.write("\n")
                        f.write(str(comment_person_name))
                        f.write("\n")

                    if len(final_number) >= 5:
                        f.write("------ CORRESPONDING MOBILE NUMBER -----")
                        f.write("\n")
                        f.write(str(final_number))
                        f.write("\n")

                    if len(final_email) >= 5:
                        f.write("------ CORRESPONDING EMAIL ID -----")
                        f.write("\n")
                        f.write(str(final_email))
                        f.write("\n")

                    if len(final_email) >= 5 or len(final_number) >= 5:
                        f.write("-----------------------------*********************----------------------------")
                        f.write("\n")
                        f.write("\n")

        if i + 1 + starting_post_no == maximum_posts:
            break

    f.close()


def get_all_posts(graph_url, app_id, app_secret, maximum_posts):
    post_url = get_graph_url(graph_url, app_id, app_secret)
    json_post_data = get_json_response(post_url)
    fb_posts = json_post_data['data']
    total_downloaded = 0
    write_posts_to_a_file(fb_posts, maximum_posts, total_downloaded)
    total_downloaded += len(fb_posts)
    fb_posts = []

    while 'paging' in json_post_data.keys() and 'next' in json_post_data['paging'].keys() and total_downloaded < maximum_posts:
        post_url = json_post_data['paging']['next']
        json_post_data = get_json_response(post_url)
        fb_posts.extend(json_post_data['data'])
        write_posts_to_a_file(fb_posts, maximum_posts, total_downloaded)
        total_downloaded += len(fb_posts)
        fb_posts = []


def main():

    app_id = '416379438547915'
    app_secret = 'e1c66cb8409855dcf19bf01cb8bdcd6a'
    print(" -----------------------------******************************************* ----------------------------")
    print(" ----- To use this crawler , you need to have the GROUP ID  of the PUBLIC GROUP that you want to "
           "crawl ----- ")
    print(" ----- Open this URL \"https://lookup-id.com/\" if you do not know the group id and enter the group "
           "link  -----")
    print(" ----- If You do not enter the group id , then the posts of the following group "
           "\"https://www.facebook.com/groups/sonia1234\" will be crawled -----")
    group_id_user = input(" ----- Enter the Group ID of the group that you want to crawl :")
    if len(group_id_user) is not 0:
        group_id = group_id_user
    else:
        print(" ----- Crawling the default Group whose url is \"https://www.facebook.com/groups/sonia1234\" -----")
        group_id = '196589213875998'
    graph_url = "https://graph.facebook.com/" + group_id
    maximum_posts = (input(" ----- Enter the maximum number of posts :"))
    f = open('posts.txt', 'w', encoding='utf-8')
    f.close()
    if len(str(maximum_posts)) is 0:
        print(" ----- Downloading default Number of posts which is %s ------" % str(100))
        maximum_posts = 100
    else:
        maximum_posts = int(maximum_posts)
    get_all_posts(graph_url, app_id, app_secret, maximum_posts)


if __name__ == "__main__":
    main()
