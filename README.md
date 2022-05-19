# Interchangeable Company Logo 

A initial Rasa bot demo implementing script 

INTRO

Hi there! I’m Company X-Bot, a new platform “Company X has commissioned to gather insights from employees across the company. Your leadership has asked me to chat with you about your experience working at Company X so they can continue to make improvements to your employee experience.

BUILD THE PROFILE

To get started, in which of company X’s regions do you work?

[continent region]

Great, thanks for that.  How would you describe your current role?

[role]

Ok, let’s jump in. 

CAPTURE PROBLEM DATA

Generally speaking, can you describe how Company X appreciates you or values you and the work you do?

[positive] - appreciated path

[negative] - not_appreciated path

Appreciated Path

Ok, let’s dig into that a bit deeper.  Can you tell me any more details about how Company X makes you feel appreciated or valued at work?

[appreciated]

That’s great, thanks.

Why do you feel this is so important to you?

[importance]

Not_appreciated Path

Sorry to hear that.

I’d like to know a little more. Can you please tell me about a specific time when you felt unappreciated or undervalued?

[problem]

Thanks so much for sharing.

Let’s pretend this was magically solved tomorrow.  Beyond feeling more valued, what else would change for you at Company X?

[desired_outcome]

Ok, got it. 

Second Pass?

Would you like to keep discussing your experience working at CompanyX?

[yes]

That’s great, let’s do it.

[jump to] CAPTURE PROBLEM DATA

[no] WRAP-UP

WRAP-UP

Well, thanks so much for chatting with me today! I’ll get all of your info compiled with your fellow employees to ensure Company X’s leadership has a solid perspective from all of its employees. 

## Deployment

```
pip install rasa
pip install fuzzywuzzy
```

## Running chatbot

```
rasa train
rasa run actions & rasa shell

or 

rasa run actions & rasa interactive
```

when shell/interactive starts type 'start' for the interview


## Using demo chatbot in browser

```
rasa train
rasa run actions
rasa run --cors "*" --enable-api
```

then open demo-ui/index.html in browser (chrome)