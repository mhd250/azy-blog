var posts=["2026/02/27/hello-world/","2026/02/27/未来/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };