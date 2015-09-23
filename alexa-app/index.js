var http       = require('http')
  , AlexaSkill = require('./AlexaSkill')
  , APP_ID     = 'amzn1.echo-sdk-ams.app.901a3f73-22df-4ad2-aa7c-ed49c3a07a6f'
  , MTA_KEY    = 'your-mta-key';

var url = 'http://www.showertexts.com/today';


var getThoughtText = function(callback){
  http.get(url, function(res){
    var body = '';

    res.on('data', function(data){
      body += data;
    });

    res.on('end', function(){
      var result = body;
      callback(result);
    });

  }).on('error', function(e){
    console.log('Error: ' + e);
  });
};

var handleNextRequest = function(intent, session, response){
  getThoughtText(function(data){
    var heading = 'Todays shower thought.';
    response.tellWithCard(data, heading, data);
  });
};


var ShowerText = function(){
  AlexaSkill.call(this, APP_ID);
};

ShowerText.prototype = Object.create(AlexaSkill.prototype);
ShowerText.prototype.constructor = ShowerText;

ShowerText.prototype.eventHandlers.onLaunch = function(launchRequest, session, response){
  var output = 'Welcome to Shower Texts. ' +
    'I can tell you todays Shower Thought. Just ask what is todays shower thought.';

  var reprompt = 'Would you like to know todays shower thought?';

  response.ask(output, reprompt);
};


ShowerText.prototype.intentHandlers = {
  GetThoughtIntent: function(intent, session, response){
    handleNextRequest(intent, session, response);
  },

  HelpIntent: function(intent, session, response){
    var speechOutput = 'Ask what is todays shower thought.';
    response.ask(speechOutput);
  }
};


exports.handler = function(event, context) {
    var skill = new ShowerText();
    skill.execute(event, context);
};
