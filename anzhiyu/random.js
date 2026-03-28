var posts=["2026/03/28/hello-world/","2026/03/28/未来/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };