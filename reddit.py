import praw, os, requests, sys, shutil
from cred import cred, subreddits_to_process

root_dir = './subreddits'
num_submissions_to_fetch = 1000

def download_image(url, path):
	try:
		#Check if the file already exists
		if url.endswith('.jpg'):
			for root, dirs, files in os.walk(os.path.dirname(path)):
				#Check if the basename aka submission id.jpg already exists
				if os.path.basename(path) not in files:
					#Start download using streams
					response = requests.get(url, stream=True)
					if response.status_code == 200:
						with open(path,'wb') as f:
							shutil.copyfileobj(response.raw, f)
	except Exception as e:
		print('Error occurred while downloading image :',str(e))
		sys.exit(1)

def check_dir(path):
  if not os.path.exists(path):
    os.makedirs(path,exist_ok=True)

def login(username,password,client_id,client_secret,user_agent='Test script to learn praw'):
	reddit = praw.Reddit(client_id=client_id,
	                     client_secret=client_secret,
	                     password=password,
	                     user_agent=user_agent,
	                     username=username)
	return reddit

if __name__ == '__main__':
	reddit = login(cred['username'],cred['password'],cred['client_id'],cred['client_secret'])

	for subreddit_name in subreddits_to_process:
		print('Checking through ',subreddit_name)
		dir_path = root_dir+os.sep+subreddit_name
		check_dir(dir_path)
		#Get all the top submissions from the subreddit instance
		for submission in reddit.subreddit(subreddit_name).top(limit=num_submissions_to_fetch):
				download_image(submission.url,dir_path+os.sep+submission.id+'.jpg')

	print('Done downloading all the images')