var ctx = document.getElementById('myChart').getContext('2d')

$.getJSON("./plagiarism_info.json", (data) => {
  var tot_rate = []
  for(i=1; i < 20 ; i++){
    if(i <= 10){
      fname = 'copy'
    }else{
      fname = 'e'
    }
    if(i < 10){
      fnum = '0'+String(i)
    }else if(i == 10 || i == 20){
      fnum = '10'
    }else{
      fnum = '0'+String(i-10)
    }
    tot_rate.push(data['./data/simulation_repo/['+fname+']'+fnum+'.docx']['tot_rate'])
    let url_list = []
    for(j=0; j < 30; j++){
      let rate = data['./data/simulation_repo/['+fname+']'+fnum+'.docx']['./data/webinfo/'+String(i-1)+'-'+String(j)+'.txt']['rate']
      let url = data['./data/simulation_repo/['+fname+']'+fnum+'.docx']['./data/webinfo/'+String(i-1)+'-'+String(j)+'.txt']['url']
      if(rate > 0 && url_list.indexOf(url) == -1){
        $('tbody').append(
                '<tr class="test">'+
                  '<td>'+Object.keys(data)[i-1]+'</td>'+
                  '<td>'+
                    '<a href="'+url+'">'+Object.keys(data[Object.keys(data)[i-1]])[j]+'</a>'+
                  '</td>'+
                  '<td>'+rate+'</td>'+
                '</tr>'
          )
      }
      url_list.push(url)
      url_list = Array.from(new Set(url_list))
    }
  }

  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
      datasets: [{
        data: tot_rate,
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)',],
        borderWidth: 1
      }]
    },
    options: {
      legend: {
        display: false,
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  })

  $('tr').on('click', function(){
    var compare_info = [$(this).children()[0].innerText, $(this).children()[1].innerText]
    window.location.href = './compare.html'+
                           '?report='+$(this).children()[0].innerText+
                           '&webinfo='+$(this).children()[1].innerText
  })
})

