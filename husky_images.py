import praw, os, requests, sys, shutil
from cred import cred, subreddits_to_process
from reddit import login,check_dir

reddit = login(cred['username'],cred['password'],cred['client_id'],cred['client_secret'])

images = []
image_str = ''
husky_subreddits = ['husky','siberianhusky','hipsterhuskies']
subdirectory_name = 'htmls'
file_name = subdirectory_name+os.sep+'husky.html'

check_dir(subdirectory_name)

num_submissions_to_fetch=5000

for subreddit_name in husky_subreddits:
    print('Checking through ',subreddit_name)
    #Get all the top submissions from the subreddit instance
    for submission in reddit.subreddit(subreddit_name).top(limit=num_submissions_to_fetch):
      url = submission.url
      if '.jpg' in url or url.endswith('.gif'):
            images.append(url)

image_str += '<div class="row">'+'\n'
for i in range(0,4):
	image_str += '\t<div class="column">'+'\n'
	for j in range(int(len(images)/4)*i,int(len(images)/4)*(i+1)):
		image_str += '''\t\t<img src="placeholder.gif" data-src="{}" class="modal_img lazy" style="width:100%">\n'''.format(images[j])
	image_str += '\t</div>'+'\n'
image_str += '</div>'+'\n'

html_code = """

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="corgis.css">
</head>
<body>
<div id="myModal" class="modal">
  <span class="close">&times;</span>
  <img class="modal-content" id="img01">
  <div id="caption"></div>
</div>

<!-- Header -->
<div class="header" id="myHeader">
  <h1>Image Grid</h1>
  <p>Click on the buttons to change the grid view. Click on an image to bring only that to foreground</p>
  <button class="btn" onclick="one()">1</button>
  <button class="btn" onclick="two()">2</button>
  <button class="btn active" onclick="four()">4</button>
</div>
<script src="corgis_image_grid.js"></script>

<!-- Photo Grid -->
"""+image_str+"""

<script>
	var current = document.getElementsByClassName("active");
	current[0].click();

	document.addEventListener("DOMContentLoaded", function() {
  var lazyImages = [].slice.call(document.querySelectorAll("[data-src]"));

  console.log(lazyImages)

  if ("IntersectionObserver" in window) {
    let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          let lazyImage = entry.target;
          //lazyImage.src = lazyImage.dataset.src;
          //lazyImage.srcset = lazyImage.dataset.srcset;
          lazyImage.setAttribute('src',lazyImage.getAttribute('data-src'));
          //lazyImage.classList.remove("lazy");
          lazyImageObserver.unobserve(lazyImage);
        }
      });
    });

    lazyImages.forEach(function(lazyImage) {
      lazyImageObserver.observe(lazyImage);
    });
  } else {
    // Possibly fall back to a more compatible method here
  }
});
</script>
<script src="corgis_modal.js"></script>


</body>
</html>

"""

with open(file_name,'w') as f:
	f.write(html_code)

