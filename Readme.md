Reseach agent!!
enter the information uwant ,agentwill getinformationfromtheweb andsendsbacktollmsothat
itcanenrichthecontentabsedonmutlipessourceandcombimesall inone messagethenmsavesitina..txt file


working!!
message invoke is calledfirst whehreuserpromptisgivenhereinthiscasewehavegivenTHENPROMPT"Research LangGraph and how it differs from LangChain.Then save a detailed summary to a file called langraph_summary"
after that thellmdetermieswttoolstocalll and also decides wt qeruy topass tothewebseachsearchtools
afterthatweget  responsebackfromthe webseachtool thebasedontheresponse llmenrichthemesassage onthen send then it printthemessageinterminal afterttitwillask to proceedornot,typeyes/y itwiillcreatean.txtfilewillthe informationthatwillfoundintavilyandenrichbythellm


howtorun 
first
uv venv
then
.venv\Scripts\activate
then typeyourqueryinn
result=app.invoke({
    "messages":[HumanMessage(content="enter yorquerythatuhav tofindinfoabt?")]
    
python research_agent.py
then itwillaskwhethertoproceedrnot type yes/yinternmila
itwillcreatean.txtwithyourinformationinit
