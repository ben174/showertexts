$(function() {
  $("#subscribe").click(subscribe);
  setInterval(rotateThought, 6000);
  setInterval(updateCount, 10000);
  updateCount();
  $("#sms_number").keyup(smsNumberKeyup);
});

var thoughtIndex = 0;
function smsNumberKeyup(event){
    if(event.keyCode == 13){
        $("#subscribe").focus();
        subscribe();
    }
}
function rotateThought() {
  $("#thought").removeClass('bounceInRight').addClass('bounceOutLeft');
  setTimeout(moveInThought, 1000);
}

function updateCount() {
  $.get("/count", function(data) {
    $("#count").text(data)
  });
}

function moveInThought() {
  $("#thought").text(thoughts[thoughtIndex]).removeClass('bounceOutLeft').addClass('bounceInRight');
  thoughtIndex++;
  if(thoughtIndex > thoughts.length) {
    thoughtIndex = 0;
  }
}

function subscribe() {
  $("#heading").removeClass('rubberBand').addClass('bounceOutLeft');
  $.post("/subscribe", {'sms_number': $('#sms_number').val()}, function(data) {
    $("#heading").removeClass('bounceOutLeft').html("<a href='#'>" + data + "</a>").addClass('bounceInLeft');
  });
}

thoughts = [
  'Waterboarding at Guantanamo Bay sounds super rad if you don\'t know what either of those things are.',
  'If Obama was the president of Kenya, he would be their first white president.',
  'The object of golf is to play the least amout of golf.',
  'I wonder what people who type "u" instead of "you" do with all their free time.',
  'The sinking of the Titanic must have been a miracle to the lobsters in the kitchen.',
  'Most people are buried in suits and stuff so a zombie apocalypse would be a formal event.',
  'They should announce a sequel to Groundhog Day and then just re-release the original.',
  'The person who would proof read Hitler\'s speeches was a grammar Nazi.',
  'Now that cellphones are becoming more and more waterproof, pretty soon it will be okay to push people into pools again.',
  '"Go to bed, you\'ll feel better in the morning" is the human version of "Did you turn it off and turn it back on again?"',
  'Your stomach thinks all potato is mashed.',
  'If you rip a hole in a net, there\'s actually fewer holes in it than it was before.',
  'When you drink alcohol you are just borrowing happiness from tomorrow.',
  'I have never once hit the space bar while watching a YouTube video with the intention of scrolling halfway down the page',
  'If Goldilocks tried three beds, then Momma Bear and Daddy Bear slept seperately. Baby Bear is probably the only thing keeping the family together.',
  'Maybe "Are You Smarter Than a 5th Grader?" isn\'t a show that displays how stupid grown adults can be, but rather, a show that depicts how much useless information we teach grade schoolers that won\'t be retained or applicable later in life.',
  'Instead of all the prequel and sequel movies coming out, they should start making equels - films shot in the same time period as the original film, but from an entirely different perspective',
  'Everyday, someone on Earth unknowingly does the biggest poo in the world for that day.',
  '"Would you rather crash on a friend\'s couch or the freeway?" would be a good campaign slogan against drinking and driving.',
  'No \'how I made a million dollars\' books include the author starting their journey to wealth by reading a book about how to make a million dollars.',
  'Websites should post their password requirements on their login pages so I can remember WTF I needed to do to my normal password to make it work on their site',
  'Is it crazy how saying sentences backwards creates backwards sentences saying how crazy it is?',
  'Thanks to the Internet, I have probably seen more naked ladies than all of my ancestors combined.',
  'I wish I had a Mario Kart-like ghost of myself punctually getting ready for work in the morning so I\'d know if I was running late.',
  'I should ask my barber where he gets his hair cut, then go there and slowly make my way up the chain until I find THE GREATEST BARBER IN THE WORLD...or perhaps just a bald dude.',
  'I used hola unblocker to watch Argo on the Canadian Netflix. I was an American who had to pretend to be Canadian to watch a movie about Americans who have to pretend to be Canadians making a movie.',
  'The real unsung hero in School Of Rock is the promoter who got about 2,000 people to a local Battle Of The Bands on a weekday morning.',
  'Coming from a big family, I don\'t know what is more sad - That one of us will have to go to seven funerals, or that one of us won\'t have to go to any.',
  'In the future, imagine how many Go-Pros will be found in snow mountains containing the last moments of peoples lives.',
  'Since smart watches can now read your pulse, there should be a feature that erases your browser history if your heart stops beating.',
]
