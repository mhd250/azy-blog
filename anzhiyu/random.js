var posts=["2026/03/21/hello-world/","2026/03/21/未来/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };