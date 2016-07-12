Search.setIndex({envversion:47,filenames:["handlers/index","index","internals/index","internals/modules","internals/nautilus.api","internals/nautilus.api.endpoints","internals/nautilus.api.endpoints.requestHandlers","internals/nautilus.api.util","internals/nautilus.auth","internals/nautilus.auth.models","internals/nautilus.auth.models.fields","internals/nautilus.auth.models.mixins","internals/nautilus.auth.primitives","internals/nautilus.auth.requestHandlers","internals/nautilus.auth.requestHandlers.forms","internals/nautilus.config","internals/nautilus.contrib","internals/nautilus.contrib.graphene_peewee","internals/nautilus.conventions","internals/nautilus.management","internals/nautilus.management.scripts","internals/nautilus.management.util","internals/nautilus.models","internals/nautilus.models.fields","internals/nautilus.models.serializers","internals/nautilus.network","internals/nautilus.network.events","internals/nautilus.network.events.actionHandlers","internals/nautilus.network.events.consumers","internals/nautilus.network.http","internals/nautilus.services","intro/api","intro/auth","intro/auth_old","intro/connecting_services","intro/first_model","intro/first_service","intro/index","intro/installation","schema/index","services/index","utilities/index"],objects:{"":{nautilus:[2,0,0,"-"]},"nautilus.APIGateway":{action_handler:[40,4,1,""],api_request_handler_class:[40,4,1,""]},"nautilus.AuthService":{init_db:[40,3,1,""]},"nautilus.ModelService":{get_models:[40,3,1,""],init_db:[40,3,1,""]},"nautilus.Service":{add_http_endpoint:[40,3,1,""],announce:[40,3,1,""],cleanup:[40,3,1,""],route:[40,5,1,""],run:[40,3,1,""]},"nautilus.api":{endpoints:[5,0,0,"-"],filter:[4,0,0,"-"],schema:[4,0,0,"-"],util:[7,0,0,"-"]},"nautilus.api.endpoints":{requestHandlers:[6,0,0,"-"]},"nautilus.api.endpoints.requestHandlers":{apiQuery:[6,0,0,"-"],graphiql:[6,0,0,"-"],graphql:[6,0,0,"-"]},"nautilus.api.endpoints.requestHandlers.apiQuery":{APIQueryHandler:[6,1,1,""]},"nautilus.api.endpoints.requestHandlers.graphiql":{GraphiQLRequestHandler:[6,1,1,""]},"nautilus.api.endpoints.requestHandlers.graphiql.GraphiQLRequestHandler":{get:[6,3,1,""]},"nautilus.api.endpoints.requestHandlers.graphql":{GraphQLRequestHandler:[6,1,1,""]},"nautilus.api.endpoints.requestHandlers.graphql.GraphQLRequestHandler":{get:[6,3,1,""],post:[6,3,1,""],request_context:[6,4,1,""],schema:[6,4,1,""],service:[6,4,1,""]},"nautilus.api.filter":{args_for_model:[4,2,1,""],filter_model:[4,2,1,""]},"nautilus.api.schema":{Schema:[4,1,1,""]},"nautilus.api.util":{create_model_schema:[7,0,0,"-"],fields_for_model:[7,0,0,"-"],generate_api_schema:[7,0,0,"-"],graphql_type_from_summary:[7,0,0,"-"],parse_string:[7,0,0,"-"],walk_query:[7,0,0,"-"]},"nautilus.api.util.create_model_schema":{create_model_schema:[7,2,1,""]},"nautilus.api.util.fields_for_model":{fields_for_model:[7,2,1,""]},"nautilus.api.util.generate_api_schema":{generate_api_schema:[7,2,1,""]},"nautilus.api.util.graphql_type_from_summary":{graphql_type_from_summary:[7,2,1,""]},"nautilus.api.util.parse_string":{parse_string:[7,2,1,""]},"nautilus.api.util.walk_query":{walk_query:[7,2,1,""]},"nautilus.auth":{decorators:[8,0,0,"-"],models:[9,0,0,"-"],primitives:[12,0,0,"-"],random_string:[8,2,1,""],requestHandlers:[13,0,0,"-"]},"nautilus.auth.decorators":{login_required:[8,2,1,""]},"nautilus.auth.models":{fields:[10,0,0,"-"],mixins:[11,0,0,"-"],userPassword:[9,0,0,"-"]},"nautilus.auth.models.fields":{password:[10,0,0,"-"]},"nautilus.auth.models.fields.password":{PasswordField:[10,1,1,""]},"nautilus.auth.models.fields.password.PasswordField":{db_field:[10,4,1,""],db_value:[10,3,1,""],python_value:[10,3,1,""]},"nautilus.auth.models.mixins":{hasPassword:[11,0,0,"-"],user:[11,0,0,"-"]},"nautilus.auth.models.mixins.hasPassword":{HasPassword:[11,1,1,""]},"nautilus.auth.models.mixins.hasPassword.HasPassword":{DoesNotExist:[11,4,1,""],id:[11,4,1,""],model_name:[11,4,1,""],password:[11,4,1,""]},"nautilus.auth.models.mixins.user":{User:[11,1,1,""]},"nautilus.auth.models.mixins.user.User":{DoesNotExist:[11,4,1,""],email:[11,4,1,""],firstname:[11,4,1,""],id:[11,4,1,""],lastname:[11,4,1,""],model_name:[11,4,1,""]},"nautilus.auth.models.userPassword":{UserPassword:[9,1,1,""]},"nautilus.auth.models.userPassword.UserPassword":{DoesNotExist:[9,4,1,""],id:[9,4,1,""],model_name:[9,4,1,""],password:[9,4,1,""],user:[9,4,1,""]},"nautilus.auth.primitives":{passwordHash:[12,0,0,"-"]},"nautilus.auth.primitives.passwordHash":{PasswordHash:[12,1,1,""]},"nautilus.auth.primitives.passwordHash.PasswordHash":{"__eq__":[12,3,1,""],"__repr__":[12,3,1,""],"new":[12,5,1,""],coerce:[12,5,1,""],rehash:[12,3,1,""]},"nautilus.auth.requestHandlers":{base:[13,0,0,"-"],forms:[14,0,0,"-"],login:[13,0,0,"-"],logout:[13,0,0,"-"],register:[13,0,0,"-"]},"nautilus.auth.requestHandlers.base":{AuthRequestHandler:[13,1,1,""]},"nautilus.auth.requestHandlers.base.AuthRequestHandler":{get_current_user:[13,3,1,""],login_user:[13,3,1,""],logout_user:[13,3,1,""]},"nautilus.auth.requestHandlers.forms":{change:[14,0,0,"-"],forgot:[14,0,0,"-"],login:[14,0,0,"-"],register:[14,0,0,"-"]},"nautilus.auth.requestHandlers.forms.change":{ChangePasswordForm:[14,1,1,""]},"nautilus.auth.requestHandlers.forms.change.ChangePasswordForm":{password:[14,4,1,""],password_again:[14,4,1,""],validate_password_again:[14,3,1,""]},"nautilus.auth.requestHandlers.forms.forgot":{ForgotPasswordForm:[14,1,1,""]},"nautilus.auth.requestHandlers.forms.forgot.ForgotPasswordForm":{email:[14,4,1,""]},"nautilus.auth.requestHandlers.forms.login":{LoginForm:[14,1,1,""]},"nautilus.auth.requestHandlers.forms.login.LoginForm":{email:[14,4,1,""],password:[14,4,1,""]},"nautilus.auth.requestHandlers.forms.register":{RegistrationForm:[14,1,1,""]},"nautilus.auth.requestHandlers.forms.register.RegistrationForm":{email:[14,4,1,""],password:[14,4,1,""]},"nautilus.auth.requestHandlers.login":{LoginHandler:[13,1,1,""]},"nautilus.auth.requestHandlers.login.LoginHandler":{get:[13,3,1,""],post:[13,3,1,""]},"nautilus.auth.requestHandlers.logout":{LogoutHandler:[13,1,1,""]},"nautilus.auth.requestHandlers.logout.LogoutHandler":{get:[13,3,1,""]},"nautilus.auth.requestHandlers.register":{RegisterHandler:[13,1,1,""]},"nautilus.auth.requestHandlers.register.RegisterHandler":{get:[13,3,1,""],post:[13,3,1,""]},"nautilus.config":{config:[15,0,0,"-"]},"nautilus.config.config":{Config:[15,1,1,""]},"nautilus.config.config.Config":{"__getattr__":[15,3,1,""],"__setattr__":[15,3,1,""]},"nautilus.contrib":{graphene_peewee:[17,0,0,"-"]},"nautilus.contrib.graphene_peewee":{converter:[39,2,1,""],objectType:[17,0,0,"-"]},"nautilus.contrib.graphene_peewee.converter":{convert_field_to_bool:[17,2,1,""],convert_field_to_float:[17,2,1,""],convert_field_to_int:[17,2,1,""],convert_field_to_pk:[17,2,1,""],convert_field_to_string:[17,2,1,""],convert_peewee_field:[17,2,1,""]},"nautilus.contrib.graphene_peewee.objectType":{PeeweeObjectType:[17,1,1,""],PeeweeObjectTypeMeta:[17,1,1,""],PeeweeObjectTypeOptions:[17,1,1,""]},"nautilus.contrib.graphene_peewee.objectType.PeeweeObjectType":{List:[17,4,1,""],NonNull:[17,4,1,""],model:[17,4,1,""]},"nautilus.contrib.graphene_peewee.objectType.PeeweeObjectTypeMeta":{construct:[17,3,1,""],options_class:[17,4,1,""]},"nautilus.contrib.graphene_peewee.objectType.PeeweeObjectTypeOptions":{contribute_to_class:[17,3,1,""]},"nautilus.conventions":{actions:[18,0,0,"-"],api:[18,0,0,"-"],auth:[18,0,0,"-"],models:[18,0,0,"-"],services:[18,0,0,"-"]},"nautilus.conventions.actions":{change_action_status:[18,2,1,""],error_status:[18,2,1,""],get_crud_action:[18,2,1,""],hydrate_action:[18,2,1,""],intialize_service_action:[18,2,1,""],pending_status:[18,2,1,""],roll_call_type:[18,2,1,""],serialize_action:[18,2,1,""],success_status:[18,2,1,""]},"nautilus.conventions.api":{root_query:[18,2,1,""]},"nautilus.conventions.auth":{cookie_name:[18,2,1,""]},"nautilus.conventions.models":{get_model_string:[18,2,1,""],normalize_string:[18,2,1,""]},"nautilus.conventions.services":{api_gateway_name:[18,2,1,""],auth_service_name:[18,2,1,""],connection_service_name:[18,2,1,""],model_service_name:[18,2,1,""]},"nautilus.database":{init_db:[2,2,1,""]},"nautilus.management":{scripts:[20,0,0,"-"],util:[21,0,0,"-"]},"nautilus.management.scripts":{create:[20,0,0,"-"]},"nautilus.management.util":{render_template:[21,2,1,""]},"nautilus.models":{base:[22,0,0,"-"],fields:[23,0,0,"-"],serializers:[24,0,0,"-"],util:[22,0,0,"-"]},"nautilus.models.base":{BaseModel:[22,1,1,""]},"nautilus.models.base.BaseModel":{DoesNotExist:[22,4,1,""],fields:[22,5,1,""],id:[22,4,1,""],model_name:[22,4,1,""],primary_key:[22,5,1,""],required_fields:[22,5,1,""]},"nautilus.models.serializers":{modelSerializer:[24,0,0,"-"]},"nautilus.models.serializers.modelSerializer":{ModelSerializer:[24,1,1,""]},"nautilus.models.serializers.modelSerializer.ModelSerializer":{"default":[24,3,1,""],serialize:[24,3,1,""]},"nautilus.models.util":{create_connection_model:[22,2,1,""]},"nautilus.network":{events:[26,0,0,"-"],http:[29,0,0,"-"]},"nautilus.network.events":{actionHandlers:[27,0,0,"-"],consumers:[28,0,0,"-"],util:[26,0,0,"-"]},"nautilus.network.events.actionHandlers":{createHandler:[27,0,0,"-"],create_handler:[0,2,1,""],crudHandler:[27,0,0,"-"],crud_handler:[0,2,1,""],deleteHandler:[27,0,0,"-"],delete_handler:[0,2,1,""],noop_handler:[27,2,1,""],readHandler:[27,0,0,"-"],read_handler:[0,2,1,""],rollCallHandler:[27,0,0,"-"],roll_call_handler:[0,2,1,""],updateHandler:[27,0,0,"-"],update_handler:[0,2,1,""]},"nautilus.network.events.actionHandlers.createHandler":{create_handler:[27,2,1,""]},"nautilus.network.events.actionHandlers.crudHandler":{crud_handler:[27,2,1,""]},"nautilus.network.events.actionHandlers.deleteHandler":{delete_handler:[27,2,1,""]},"nautilus.network.events.actionHandlers.readHandler":{read_handler:[27,2,1,""]},"nautilus.network.events.actionHandlers.rollCallHandler":{roll_call_handler:[27,2,1,""]},"nautilus.network.events.actionHandlers.updateHandler":{update_handler:[27,2,1,""]},"nautilus.network.events.consumers":{actions:[28,0,0,"-"],api:[28,0,0,"-"],kafka:[28,0,0,"-"]},"nautilus.network.events.consumers.actions":{ActionHandler:[28,1,1,""]},"nautilus.network.events.consumers.actions.ActionHandler":{consumer_channel:[28,4,1,""],handle_action:[28,3,1,""],handle_message:[28,3,1,""],producer_channel:[28,4,1,""],server:[28,4,1,""]},"nautilus.network.events.consumers.api":{APIActionHandler:[28,1,1,""]},"nautilus.network.events.consumers.api.APIActionHandler":{consumer_pattern:[28,4,1,""],handle_action:[28,3,1,""]},"nautilus.network.events.consumers.kafka":{KafkaBroker:[28,1,1,""]},"nautilus.network.events.consumers.kafka.KafkaBroker":{ask:[28,3,1,""],consumer_channel:[28,4,1,""],consumer_pattern:[28,4,1,""],handle_message:[28,3,1,""],initial_offset:[28,4,1,""],loop:[28,4,1,""],producer_channel:[28,4,1,""],send:[28,3,1,""],server:[28,4,1,""],start:[28,3,1,""],stop:[28,3,1,""]},"nautilus.network.events.util":{combine_action_handlers:[26,2,1,""]},"nautilus.network.http":{requestHandler:[29,0,0,"-"],respones:[29,0,0,"-"]},"nautilus.network.http.requestHandler":{RequestHandler:[29,1,1,""]},"nautilus.network.http.requestHandler.RequestHandler":{options:[29,3,1,""],post:[29,3,1,""]},"nautilus.services":{apiGateway:[30,0,0,"-"],authService:[30,0,0,"-"],connectionService:[30,0,0,"-"],modelService:[30,0,0,"-"],service:[30,0,0,"-"],serviceManager:[30,0,0,"-"]},"nautilus.services.apiGateway":{APIGateway:[30,1,1,""]},"nautilus.services.apiGateway.APIGateway":{action_handler:[30,4,1,""],announce:[30,3,1,""],api_request_handler_class:[30,4,1,""],init_routes:[30,3,1,""],name:[30,4,1,""]},"nautilus.services.authService":{AuthService:[30,1,1,""],Login:[30,1,1,""],Logout:[30,1,1,""],Register:[30,1,1,""]},"nautilus.services.authService.AuthService":{get_models:[30,3,1,""],init_db:[30,3,1,""],name:[30,4,1,""]},"nautilus.services.connectionService":{ConnectionService:[30,1,1,""]},"nautilus.services.connectionService.ConnectionService":{action_handler:[30,4,1,""],from_service:[30,4,1,""],name:[30,4,1,""],summarize:[30,3,1,""],to_service:[30,4,1,""]},"nautilus.services.modelService":{ModelService:[30,1,1,""]},"nautilus.services.modelService.ModelService":{action_handler:[30,4,1,""],get_models:[30,3,1,""],init_db:[30,3,1,""],model:[30,4,1,""],name:[30,4,1,""],summarize:[30,3,1,""]},"nautilus.services.service":{Service:[30,1,1,""],ServiceActionHandler:[30,1,1,""],ServiceMetaClass:[30,1,1,""]},"nautilus.services.service.Service":{action_handler:[30,4,1,""],add_http_endpoint:[30,3,1,""],announce:[30,3,1,""],api_request_handler_class:[30,4,1,""],cleanup:[30,3,1,""],config:[30,4,1,""],init_action_handler:[30,3,1,""],init_app:[30,3,1,""],init_routes:[30,3,1,""],name:[30,4,1,""],route:[30,5,1,""],run:[30,3,1,""],schema:[30,4,1,""],summarize:[30,3,1,""]},"nautilus.services.service.ServiceActionHandler":{handle_action:[30,3,1,""]},"nautilus.services.serviceManager":{ServiceManager:[30,1,1,""]},"nautilus.services.serviceManager.ServiceManager":{run:[30,3,1,""]},nautilus:{APIGateway:[40,1,1,""],AuthService:[40,1,1,""],ConnectionService:[40,1,1,""],ModelService:[40,1,1,""],Service:[40,1,1,""],api:[4,0,0,"-"],auth:[8,0,0,"-"],config:[15,0,0,"-"],contrib:[16,0,0,"-"],conventions:[18,0,0,"-"],database:[2,0,0,"-"],management:[19,0,0,"-"],models:[22,0,0,"-"],network:[25,0,0,"-"],services:[30,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","function","Python function"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","classmethod","Python class method"]},objtypes:{"0":"py:module","1":"py:class","2":"py:function","3":"py:method","4":"py:attribute","5":"py:classmethod"},terms:{"0x108d752b0":14,"0x108fea8d0":14,"0x108fea9b0":14,"__eq__":12,"__getattr__":15,"__main__":[31,34,36],"__name__":[31,34,36],"__naut_nam":7,"__repr__":12,"__setattr__":15,"abstract":12,"case":39,"class":[0,4,6,9,10,11,12,13,14,15,17,22,24,28,29,30,31,33,34,35,36,39,40],"default":[10,18,24,28,30,40],"final":36,"function":[0,2,7,10,13,18,21,24,26,27,28,30,33,34,36,39,40],"import":[0,28,29,30,31,33,34,35,36,39,40],"int":[10,30,40],"new":[0,12,14,27,31,33,34,39],"null":10,"return":[0,7,10,18,22,27,30,33,39,40],"true":[24,30,33,40],"try":[35,36],"while":[1,10,31],abl:[31,33,39],about:[1,30,36,40],abov:0,access:[30,40],accord:40,account:33,act:[30,40],action_handl:[0,30,36,40],action_handler1:0,action_handler2:0,action_typ:[0,18,27,28,30,36],actionhandl:[0,2,25,26],actiontyp:36,actual:34,add:[0,10,33,34],add_http_endpoint:[30,40],address:14,administr:1,again:[14,34],against:[0,27,28],ahead:33,aiohttp:29,alchemi:22,alia:[9,11,17,22,30,40],all:[1,26,30,31,33,40],all_servic:18,allow:[10,15,28],allow_nan:24,also:[28,34],although:39,ani:[10,30,31,35,36,40],announc:[28,30,31,40],annoy:31,anoth:[33,34,36,39],answer:28,anyth:36,api:[0,1,2],api_gateway_nam:18,api_request_handler_class:[30,40],apiactionhandl:[28,30,40],apigatewai:2,apiqueri:[2,4,5],apiqueryhandl:[6,30,40],app:35,applic:[1,31,33,35,36],appropri:[6,17,34,36],apt:38,architectur:36,arg:[0,4,9,11,15,17,18,22,30,40],args_for_model:4,argument:[0,21,33],arriv:0,ask:28,aspect:1,associ:[0,36],assum:[0,27],async:[0,28,29,36],asynchron:4,attr:15,attribut:[15,30],auth:[2,6],auth_service_nam:18,authent:[1,30],author:31,authrequesthandl:[6,13],authservic:2,auto_camelcas:4,automat:[30,35,40],avail:[20,38],awesom:[30,40],awesomefield:39,awesomepackag:39,ayncio:28,background:37,base:[1,2,4,6,7,8,9,10,11,12],basemodel:[0,7,9,11,22,27,30,34,35,40],basemodeldoesnotexist:22,basi:[30,40],basic:[13,30,33,40],becaus:34,been:1,befor:[14,31,35],begin:[31,33,35,36],behavior:36,behind:31,benefit:31,best:1,between:[18,30,33,34,36,40],bigdata_hadoop_zookeeper_kafka_single_node_single_broker_clust:38,bit:[31,33],block:[36,40],blog:35,bogotobogo:38,boilerpl:39,both:14,box:1,broker:28,brought:[0,27],build:[1,28,36,40],bulk:33,call:[0,26,27,28,30,31,33,34,35,40],callback:[30,40],can:[0,1,10,30,33,34,35,36,40],candid:12,cannot:33,care:39,cat:35,catphoto:[31,33,35],catphotoapi:31,catphotoservic:35,central:18,certain:36,chang:[2,8,13],change_action_statu:18,changepasswordform:14,channel:28,charfield:[9,11,30,34,35,40],check:34,check_circular:24,chmod:36,classifi:[0,34],classmethod:[12,22,30,40],classtyp:17,cleanup:[30,40],clear:13,cli:35,client:[30,33,36,40],cloud:[1,20,30,31,33,34,36,38,40],code:[34,35],coerc:12,collect:[7,30,40],column:[34,39],com:[35,38],combine_action_handl:[0,26],combined_handl:0,come:[32,37],command:30,comment:34,commentconnect:34,commentservic:34,common:[1,34,35,40],commun:[28,39],compar:12,compat:39,complain:36,complet:[31,36],complex:0,comput:36,config:2,configur:[15,30,36,40],congratul:36,connect:[7,18,22,30,33],connection_resolv:7,connection_service_nam:18,connectionservic:2,consist:[30,40],consol:36,construct:[1,17,36],consum:[2,25,26],consumer_channel:28,consumer_pattern:28,contain:34,context:[21,30],contrib:2,contribute_to_class:17,contributit:31,convent:[0,2],convert:[2,10,16],convert_column_to_str:39,convert_field_to_bool:17,convert_field_to_float:17,convert_field_to_int:17,convert_field_to_pk:17,convert_field_to_str:17,convert_peewee_field:17,convet:[0,27],cooki:13,cookie_nam:18,copi:36,core:[4,17,30,40],correct:39,correspond:[7,10,34],could:33,creat:[0,2,4,7,12,15,19],create_connection_model:22,create_handl:[0,27],create_model_schema:[2,4],create_recip:0,createhandl:[2,25,26],creator:0,credenti:[30,33,40],crud:[0,27],crud_handl:[0,27,30,40],crudhandl:[2,25,26],current:[13,33],custom:[0,39],data:[0,1,4,6,10,14,18,30,31],databas:[0,1],database_url:[2,30,33,34,35,40],databs:10,db_field:10,db_valu:10,deal:26,decor:2,deduc:[30,40],def:[0,28,29,30,33,36,39,40],defin:[0,11,17,20,26,30,35,39],definit:[17,35],delet:[0,27,30,40],delete_handl:[0,27],delete_recip:0,deletehandl:[2,25,26],describ:[0,31,36],descript:39,desgin:21,design:[18,21,30],dev:38,develop:1,dict:[7,15,21,30,40],dictionari:[0,7],differ:31,difficulti:31,directori:[21,31,33,34,35,36],dispatch:27,distribut:[1,30],doc:39,doe:[30,31,36,39,40],doesn:36,doesnotexist:[9,11,22],don:14,done:35,dummi:34,each:[0,31,35],earliest:28,easi:[10,33,35],easili:[17,39],editor:36,either:35,elif:0,email:[11,14,36],emit:[0,27,30,40],empti:36,encapsult:[30,40],encod:24,encount:31,encrypt:10,endpoint:[2,4],ensur:[12,14],ensure_ascii:24,enter:[33,34,35],entir:[30,31,40],entiti:36,entri:[33,34],equal:[10,12],error:7,error_statu:18,even:36,event:[0,2,4,25],eventloop:28,eventu:33,everi:[0,28,33],everyon:33,exact:34,exampl:[0,10,28,29,30,33,34,36,40],excel:39,execut:[6,35,36],executor:4,exist:[14,28,30,40],express:34,extend:[1,40],extern:[30,31,34],extra_field:[18,30],facebook:35,fals:[18,24,33],familiar:34,far:31,favorit:36,featur:1,feel:34,few:[31,38],field:[2,4,7,8,9],field_nam:7,fields_for_model:[2,4],file:[11,18,31,33,34,35,36],filter:2,filter_model:4,find:[0,39],finish:[29,30,40],fire:[0,30,36,40],first:0,firstnam:11,fit:1,flux:1,focu:1,follow:[0,27,31,33,34,35,36,39],foo:35,forgot:[2,8,13],forgotpasswordform:14,form:[2,8,13],format:28,formdata:14,found:33,framework:1,free:34,from:[0,12,28,29,30,31,33,34,35,36,39,40],from_servic:[30,34,40],functool:17,fundament:36,gatewai:[0,1,18,27,30,31,33],gener:[15,17,30,35,39,40],generate_api_schema:[2,4],get:[0,6,13,29,30],get_crud_act:18,get_current_us:13,get_model:[30,40],get_model_str:18,github:35,given:[0,2,12,13,18,21,24,26,30,33,34,40],global:[2,40],good:[34,40],graphen:[4,17,39],graphene_peewe:[2,16],graphiql:[2,4,5],graphiqlrequesthandl:6,graphql:[0,2,4,5],graphql_type_from_summari:[2,4],graphqlrequesthandl:[6,30],graphqlschema:[30,40],graphqltyp:7,great:34,greater:38,had:[33,36],hadoop:38,hand:6,handl:[10,13,28,30,35,40],handle_act:[0,28,30,36],handle_messag:28,hash:[10,12],hash_:12,haspassword:[2,8,9],haspassworddoesnotexist:11,have:[1,30,31,34,36,38,40],hello:[29,30,40],helloworld:[30,40],helper:17,here:[35,38],hidden:31,hide:33,highli:34,hold:36,hord:35,host:[30,40],how:[0,1,10,36,38],html:35,http:[2,6,13,25],hydrate_act:18,identifi:[33,36],ignor:36,illustr:[34,36],implement:[1,17,40],includ:[1,38],increas:10,indent:24,indic:[30,33,40],inform:[7,30,31,33,35,38,39,40],ingredi:[34,35],init:28,init_action_handl:30,init_app:30,init_db:[2,30,40],init_rout:30,initi:[2,14],initial_offset:28,inputrequir:14,insid:34,instal:37,instanc:[0,27,36],instead:31,inted:33,intefac:[30,40],intention:[30,40],interact:[17,28,33,35,39],interfac:[28,35],intern:[0,6,12,15,27,31,34,39,40],intialize_service_act:18,introduct:35,intstruct:31,invidu:[30,40],itself:39,javascript:36,join:34,json:[24,35],jsonencod:24,just:[0,31,33,35],kafka:[2,25,26],kafkabrok:28,keep:34,kei:[12,15,22,30,40],know:10,known:[31,35],kwarg:[9,11,14,17,22,30,40],kwd:[0,4,10,15,17,18,27,28,30,40],languag:1,larg:31,lastnam:11,latest:28,layer:10,learn:36,left:[10,35],length:8,less:33,let:[31,33,34,35,36],libffi:38,libssl:38,like:[0,15,31,33,35,36,39],limit:33,line:36,link:[30,40],list:[0,7,17,30,31,40],listen:[28,30,40],littl:1,live:33,load:12,local:[30,35,38,40],localhost:[28,30,35,40],locat:28,log:[13,14,33],logic:33,login:[2,8],login_requir:8,login_us:13,loginform:14,loginhandl:[13,30],logout:[2,8],logout_us:13,logouthandl:[13,30],look:[0,1,33,35,39],loop:28,machin:38,made:[33,34,35],maintain:[6,30,31,33,35,36,39,40],major:31,make:[14,30,34,36,40],manag:[2,18],mani:[31,34],map:7,massiv:1,match:[0,7,14,28,30,39,40],meant:36,member:34,messag:[1,28],meta:14,method:[13,15,18,28,30,36,40],microservic:1,might:39,mind:[34,36],mix:0,mixin:[2,8,9],mkdir:36,model:[0,2,4,7,8],model_nam:[9,11,22],model_service_nam:18,modelseri:[2,22],modelservic:2,moment:1,more:[0,1,34,35,36,38],most:39,move:1,much:36,must:38,mutat:[0,27,30,31,40],myactionhandl:0,myapigatewai:[30,40],myauth:[30,40],myconnect:[30,40],myevent:28,mymodelservic:[30,40],myrequesthandl:29,myservic:[0,30,40],name:[0,7,10,17,18,21,27,30,40],natuilu:4,natur:[30,31,34,40],nauilu:[30,40],nautilu:0,nautilus_playground:36,navig:[33,35],necessari:[0,27,30,37],necessarili:34,need:[31,33,38,39],neither:34,network:[0,2,6,13],never:39,new_statu:18,next:[10,34,36],node:31,non:10,none:[0,4,7,12,14,17,21,24,27,28,30,40],nonnul:17,noop_handl:27,nor:[30,36,40],normal:[0,27],normalize_str:18,noth:36,notic:35,now:[1,31,33,34,35,36],number:10,obj:[7,14,24],object:[9,10,11,12,14,22,24,28,30,33,39],object_resolv:7,objecttyp:[2,16],objecttypemeta:17,objecttypeopt:17,obtain:33,occur:31,onc:35,onli:[1,30,31,33,40],open:36,opportun:34,optim:31,option:[28,29,30,40],options_class:17,order:[38,39],orm:39,other:[30,31,33,34,36,40],otherwis:[0,14],our:[31,33,34,35,36],out:[1,13,31,34],out_dir:21,output:21,outsid:36,over:[6,12,28,40],overal:[30,39,40],own:[0,34,40],panel:35,paragraph:34,paramet:[0,7,10,21,27,28,30,36,40],paramt:0,pars:6,parse_str:[2,4],part:[1,30,34,36,39,40],parti:34,partial:17,pass:[0,1,31,36],password:[2,8,9],password_again:14,passwordfield:[9,10,11,14],passwordhash:[2,8,10],past:[34,35,36],patch:[17,39],pattern:[28,39],payload:[0,18,27,28,30,36],peewe:[9,10,11,17,22,39],peeweeobjecttyp:17,peeweeobjecttypemeta:17,peeweeobjecttypeopt:17,pend:[18,28],pending_statu:18,perform:[0,10,24,27,36],permiss:36,persist:[35,36],photo:35,photo_loc:35,php:38,piec:31,pip:38,place:31,plai:34,plan:1,playground:36,point:[31,34,40],port:[30,31,40],post:[6,13,29],power:36,pre:36,predict:[30,40],prefix:14,previous:34,primari:[22,30,36,40],primary_kei:22,primarykeyfield:[9,11,22],primit:[2,8],print:[0,28,36],process:[36,37],produc:[0,1,27,28],producer_channel:28,programat:[30,40],prop:[0,27,28,36],properti:0,protect:33,purpos:[0,30,40],python3:[31,35,36],python:[1,10,30,35,36,40],python_valu:10,queri:[0,6,7,18,27,30],queryabl:31,question:28,queue:[0,4,30,40],quickli:1,rage:1,rais:14,random_str:8,rare:39,rather:31,react:[35,36],read:[0,27],read_handl:[0,27],readhandl:[2,25,26],readi:33,reaturn:[0,27],receiv:[0,27],reciev:[0,27,28,30,40],recip:[0,33,34,36],recipeactionhandl:36,recipebookauth:33,recipeservic:36,record:[30,35,36,40],recreat:12,redirect:33,reduc:39,regardless:[30,33,40],regex:28,regist:[2,8],registerhandl:[13,30],registr:[1,30,33,40],registrationform:14,registri:[30,40],rehash:12,rel:[21,35],relat:[30,40],relationship:[30,33,34,36,40],releas:1,reli:39,rememb:33,remot:[1,39],remov:[0,30,40],render:21,render_templ:21,repli:35,repres:[0,34,39],represent:12,request:[0,6,13,27,29,30,33,40],request_context:6,request_handl:[30,40],requesthandl:[2,4,5],requir:[22,33],required_field:22,reset:14,resolv:[0,4,7,27],respon:[2,25],respond:[0,27,30],respons:[0,10,13,18,29,31,33],rest:37,result:33,retriev:[1,4,14,15,22,36],right:36,role:34,roll:[0,27],roll_call_handl:[0,27],roll_call_typ:18,rollcallhandl:[2,25,26],root:18,root_queri:18,round:[10,12],rout:[29,30,40],run:[28,30,31,33,34,35,36,38,40],runserv:[31,35,36],safe:10,sai:[33,34],same:[33,34],save:[0,10],scalabl:1,schema:[0,2],schema_arg:7,script:[2,19],second:0,section:36,see:[31,33,35,36],self:[0,28,29,30,33,36,40],send:[28,31,36],send_email:36,sens:34,sent:40,separ:[0,24,33],sepeci:35,serial:[2,18,22],serialize_act:18,serv:[0,28],server:[28,30,36,40],servic:[0,1,2,6,11],service_on:[30,40],serviceactionhandl:30,serviceconfig:[30,33,34,35,40],servicemanag:2,servicemetaclass:30,serviceobjecttyp:[30,40],set:[15,33],setup:37,should:[28,31,35,39],show:39,shutdown_timeout:[30,40],simpl:12,simpli:[33,40],singl:[7,26,30,31,36,40],singledispatch:39,singleton:30,skip:34,skipkei:24,small:[30,31],sole:[30,40],solut:[0,1],solv:31,some:[0,1,34,36,40],someth:[0,10,33,39],somewher:[35,36],soon:[32,37],sort:[30,31,35,40],sort_kei:24,sourc:[0,2,4,6,7,8,9,10,11,12,13,14,15,17,18,21,22,24,26,27,28,29,30,40],span:31,spec:1,special:[34,36,39],specif:35,specifi:[0,27,33],split:0,sql:22,sqlite:[30,33,34,35,40],sqlitebrows:35,stai:1,standalon:40,standard:35,start:[28,30,31,34,36],state:[0,31,40],statu:18,stop:28,storag:10,store:[12,30,33,35,36,40],str:[7,28,30,40],stream:28,string:[0,10,12,18,21,30,39,40],stringfield:14,structur:18,success_statu:18,successfulli:[30,40],succintli:36,sudo:[36,38],summar:30,summari:[0,7,27,31,40],support:[10,17],sure:34,syncdb:35,system:[6,28,30,31,36,38,40],tabl:[22,34,35],take:[0,18,33,36,39],target_model:7,task:35,tediou:0,templat:21,test:[10,36],text:36,than:[36,38],thank:39,thankfulli:33,thei:[0,28,33],them:[26,33],themselv:36,thi:[0,2,4,7,10,11,12,13,14,15,17,18,20,21,22,24,26,27,28,30,31,33,34,35,36,39,40],think:1,third:34,those:[1,33,36],three:[31,36],through:[33,36],time:[1,10,34],tmp:[30,33,40],to_servic:[30,34,40],todo:10,togeth:[1,31],topolog:[30,40],touch:36,track:6,travers:7,triger:36,trigger:36,tune:1,twice:14,two:[0,28,30,34,40],type:[0,7,17,18,27,28,30,36,39,40],ubuntu:38,unboundfield:14,underli:[28,30,35,40],uniqu:34,unlik:31,updat:[0,10,27],update_handl:[0,27],updatehandl:[2,25,26],upgrad:10,url:[2,30,40],user:[2,8,9],user_id:33,userdoesnotexist:11,userpassword:[2,8],userpassworddoesnotexist:9,usual:33,util:[2,4],valid:[6,10,14,30,40],validate_password_again:14,validationerror:14,valu:[10,12,15,34],varchar:10,variou:[17,20,26,30,31,34,36,39],veri:[1,34,39,40],version:38,via:[35,40],view:[29,33],visit:[31,35],wai:[28,30,31,40],walk_queri:[2,4],want:[0,33,36],web:[1,35],web_urldispatch:29,well:[30,36,40],were:0,wether:35,what:1,when:[0,27,28,30,31,33,34,40],where:[28,39],whether:[30,40],which:[0,26,30,31,33,34,40],whose:34,within:[0,33],without:[1,30,36,40],work:36,workflow:14,world:[30,36,40],worri:[30,40],worth:31,would:[34,36],wrapper:12,written:33,wtform:14,www:38,you:[0,1,31,33,34,35,36,38,39],your:[0,30,31,33,34,35]},titles:["Action Handlers","Welcome to Nautilus!","nautilus package","nautilus","nautilus.api package","nautilus.api.endpoints package","nautilus.api.endpoints.requestHandlers package","nautilus.api.util package","nautilus.auth package","nautilus.auth.models package","nautilus.auth.models.fields package","nautilus.auth.models.mixins package","nautilus.auth.primitives package","nautilus.auth.requestHandlers package","nautilus.auth.requestHandlers.forms package","nautilus.config package","nautilus.contrib package","nautilus.contrib.graphene_peewee package","nautilus.conventions package","nautilus.management package","nautilus.management.scripts package","nautilus.management.util package","nautilus.models package","nautilus.models.fields package","nautilus.models.serializers package","nautilus.network package","nautilus.network.events package","nautilus.network.events.actionHandlers package","nautilus.network.events.consumers package","nautilus.network.http package","nautilus.services package","Querying The Distributed Structure","Authentication","Authentication","Connecting Services Together","Keeping Track of Data","Your First Service","Getting Started","Installation / Setup","API Gateway","Services","Utilities"],titleterms:{action:[0,18,28,36],actionhandl:27,api:[4,5,6,7,18,28,39],apigatewai:30,apiqueri:6,auth:[8,9,10,11,12,13,14,18],authent:[32,33],author:33,authservic:30,background:38,base:[13,22],chang:14,combin:0,config:15,connect:34,connectionservic:30,consum:28,content:[2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],contrib:[16,17],convent:18,convert:17,creat:20,create_model_schema:7,createhandl:27,crudhandl:27,data:[33,35],databas:2,decor:8,deletehandl:27,design:39,distribut:31,endpoint:[5,6],equival:39,event:[26,27,28],extern:39,factori:0,field:[10,23,39],fields_for_model:7,filter:4,first:36,forgot:14,form:14,gatewai:39,generate_api_schema:7,get:37,graphene_peewe:17,graphiql:6,graphql:[6,39],graphql_type_from_summari:7,handler:0,haspassword:11,http:29,instal:38,kafka:28,keep:35,login:[13,14],logout:13,manag:[19,20,21],mixin:11,model:[9,10,11,18,22,23,24,34],modelseri:24,modelservic:30,modul:[2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],nautilu:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,39],necessari:38,network:[25,26,27,28,29],objecttyp:17,packag:[2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],parse_str:7,particular:33,password:10,passwordhash:12,piec:33,primit:12,process:38,provid:0,queri:[31,35],readhandl:27,regist:[13,14],requesthandl:[6,13,14,29],respon:29,respond:36,reus:0,rollcallhandl:27,schema:[4,39],script:20,second:34,serial:24,servic:[18,30,34,36,39,40],servicemanag:30,setup:38,start:37,structur:31,submodul:[2,4,6,7,8,9,10,11,12,13,14,15,17,18,20,22,24,26,27,28,29,30],subpackag:[2,4,5,8,9,13,16,19,22,25,26],summar:39,togeth:34,track:35,updatehandl:27,user:[11,33],userpassword:9,util:[7,21,22,26,41],walk_queri:7,welcom:1,your:36}})