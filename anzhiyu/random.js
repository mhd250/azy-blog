var posts=["2026/07/19/hello-world/","2026/07/19/未来/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };