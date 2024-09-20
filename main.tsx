import blog from "https://deno.land/x/blog/blog.tsx";

blog({
  author: "凡学子",
  title: "My Blog",
  description: "The blog description.",
  avatar: "https://deno-avatar.deno.dev/avatar/83a531.svg",
  avatarClass: "rounded-full",
  links: [
    { title: "Email", url: "mailto:bot@deno.com" },
    { title: "GitHub", url: "https://github.com/denobot" },
    { title: "Twitter", url: "https://twitter.com/denobot" },
  ],
  lang: "zh",
});

// 用于deno deploy网站的部署，内容是posts文件夹下的md文件
/* 网址是：
https://lxz-blog.deno.dev/ 
https://linxz.online/
https://lxz-blog-gpfn65re8saz.deno.dev/

注意：deno只能外网访问。
*/

