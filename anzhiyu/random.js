var posts=["2026/06/05/hello-world/","2026/06/05/未来/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };