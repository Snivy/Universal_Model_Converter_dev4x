def run():
    import time,os,sys; sys.path.append('scripts')
    from data import COMMON, FORMAT, VIEWER

    COMMON.__functions=[0,0,0,0] #prevent unwanted initialization
    mods = [m for m in os.listdir('scripts') if m.endswith('.py')] #only get .py files
    print 'Testing Scripts:'
    time.sleep(0.5) #just to make it look convincing :P

    errors = 0
    for mod in mods:
        COMMON.Mod=mod.replace('.py','')
        
        try:
            if COMMON.Mod!='VIEWER':
                print COMMON.Mod
                M=__import__(COMMON.Mod) #initialize functions

                #what does the model/anim script support?
                if M.__dict__.has_key('ImportModel'): COMMON.__functions[0]=1
                else: COMMON.__functions[0]=0
                if M.__dict__.has_key('ExportModel'): COMMON.__functions[1]=1
                else: COMMON.__functions[1]=0
                if M.__dict__.has_key('ImportAnim'): COMMON.__functions[2]=1
                else: COMMON.__functions[2]=0
                if M.__dict__.has_key('ExportAnim'): COMMON.__functions[3]=1
                else: COMMON.__functions[3]=0
                
                if M.__dict__.has_key('DecodeImage'): COMMON.__imgfunctions[0]=1
                else: COMMON.__imgfunctions[0]=0
                if M.__dict__.has_key('EncodeImage'): COMMON.__imgfunctions[1]=1
                else: COMMON.__imgfunctions[1]=0
                
                reload(M) #set script
            
        except: errors += 1
            
        #prevent further unwanted initializations
        COMMON.__functions=[0,0,0,0]
        COMMON.__imgfunctions=[0,0]

    print
    print 'Model Importers: '+str(len(COMMON._Scripts[0][0]))
    print 'Model Exporters: '+str(len(COMMON._Scripts[0][1]))
    print 'Animation Importers: '+str(len(COMMON._Scripts[1][0]))
    print 'Animation Exporters: '+str(len(COMMON._Scripts[1][1]))
    print 'Image Decoders: '+str(len(COMMON._Scripts[2][0]))
    print 'Image Encoders: '+str(len(COMMON._Scripts[2][1]))
    print 'Bad Scripts: '+str(errors)
    print
    time.sleep(0.25) #just to make it look convincing :P

    try:
        print 'initializing viewer\n'
        COMMON.__CleanScripts()
        VIEWER.Init()
        
    except:
        import sys,traceback
        typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
        print
        traceback.print_exception(
            typ,val,tb#,
            #limit=2,
            #file=sys.stdout
            )
        print
        raw_input('press enter to exit.')
