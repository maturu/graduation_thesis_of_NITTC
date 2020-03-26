$.getJSON("./plagiarism_info.json", (data) => {
  var url = location.href
  params = url.split("?")[1].split("&")
  repo_path = params[0].split("=")[1]
  webinfo_path = params[1].split("=")[1]

  repo_txt = data[repo_path]['repo_txt']
  repo_similar = data[repo_path][webinfo_path]['repo_similar']
  repo_txt = repo_txt.split(repo_similar)
  console.log(repo_txt)
  repo_p = '<p class="text-break">'+repo_txt[0]+'</p>'+
           '<p class="text-danger text-break">'+repo_similar+'</p>'+
           '<p class="text-break">'+repo_txt[1]+'</p>'

  web_txt = data[repo_path][webinfo_path]['web_txt']
  web_similar = data[repo_path][webinfo_path]['web_similar']
  web_txt = web_txt.split(web_similar)
  console.log(web_txt)
  web_p = '<p class="text-break">'+web_txt[0]+'</p>'+
          '<p class="text-danger text-break">'+web_similar+'</p>'+
          '<p class="text-break">'+web_txt[1]+'</p>'

  $('#repo').append(repo_p)
  $('#webinfo').append(web_p)
})
