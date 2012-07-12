<?php
    
    
    $dossier_fichier_bilbo = "../fichierRes/";
    $dossier_fichier = "code/fichierRes/";

    
/************************************ SERVICE ****************************************/
    /*
     * Fonction getAnnotationArticle sert à generer les annotations des reference de l'article
     * @param $dossier  texte entier de l'article
     * @param $article  article à annoter
     * @return $resultat  article annoté
     */
    function getAnnotationArticle($dossier,$article) {
        global $dossier_fichier, $dossier_fichier_bilbo;
        $resultat = "test";
        
        
        #supprime les fichiers du dossier buffer
        system("rm ".$dossier_fichier."*");
        
        #ecrit le texte dans le fichier
        $fich = fopen($dossier_fichier.$article, "w"); 
        fwrite($fich, $dossier); 
        fclose($fich);
          
        #lance BILBO
        $saveRep = getcwd();
        
        chdir("code/bilbo");
        $newRep = getcwd();
        
        /*recupere les chemin sans bilbo*/
        $splitRep = split("/", $newRep);
        array_pop($splitRep);
        $newRepRes = join("/", $splitRep);
        $newRepRes .= "/fichierRes/";
        
        $res = exec("python ".$newRep."/src/mypkg/Main.py 1 ".$newRepRes." ".$newRepRes,$out,$error);
        $test = getcwd();
        chdir($saveRep);
        
        $fichier = $newRepRes."testEstCRF.xml";
        $resultat = file_get_contents($fichier);
        
        
        return $resultat;

    } 
    
    /*
     * Fonction getAnnotationNoteArticle sert à generer les annotations des notes de l'article
     * @param $dossier  texte entier de l'article
     * @param $article  article à annoter
     * @return $resultat  article annoté
     */
    function getAnnotationNoteArticle($dossier,$article) {
        global $dossier_fichier, $dossier_fichier_bilbo;
        $resultat = "test";
        
        
        #supprime les fichiers du dossier buffer
        system("rm ".$dossier_fichier."*");
        
        #ecrit le texte dans le fichier
        $fich = fopen($dossier_fichier.$article, "w"); 
        fwrite($fich, $dossier); 
        fclose($fich);
        
        #lance BILBO
        $saveRep = getcwd();
        
        chdir("code/bilbo");
        $newRep = getcwd();
        
        /*recupere les chemin sans bilbo*/
        $splitRep = split("/", $newRep);
        array_pop($splitRep);
        $newRepRes = join("/", $splitRep);
        $newRepRes .= "/fichierRes/";
        
        $res = exec("python ".$newRep."/src/mypkg/Main.py 2 ".$newRepRes." ".$newRepRes,$out,$error);
        $test = getcwd();
        chdir($saveRep);
        
        $fichier = $newRepRes."testEstCRF.xml";
        $resultat = file_get_contents($fichier);
        
        
        return $resultat;

    } 
    
    /*
     * Fonction getAnnotationUrl sert à generer les annotations des reference de l'article passer par url
     * @param $url  url ou se trouve l'article à annoter
     * @return $resultat  article annoté
     */
    function getAnnotationUrl($url) {
        global $dossier_fichier, $dossier_fichier_bilbo;
        $resultat = "";
        
        #supprime les fichiers du dossier buffer
        system("rm ".$dossier_fichier."*");
        
        #verifie que l'url donné soit  du xml sinon transforme l'url
        if(strpos($url, "tei.revues.org")){
            $urlXml = $url;
        }else{
            #verifie la forme de l'url
            # url : revue.org/562
            if(!strpos($url, "index")){
                preg_match("/(\/\/)(.*?)(\.)/", $url, $nom, PREG_OFFSET_CAPTURE);
                preg_match("/(org\/)(.*)/", $url, $id, PREG_OFFSET_CAPTURE);
                #verifie qu'il n'y est pas d'ancre ds l'url : (exemple : id#reference)
                if(strpos($id[2][0], "#")){
                    $bufId = split("#", $id[2][0]);
                    $id[2][0] = $bufId[0];
                }
                $urlXml = "http://tei.revues.org/".$nom[2][0]."-".$id[2][0].".xml";
            }else{  # url : revue.org/index562.html
                preg_match("/(\/\/)(.*?)(\.)/", $url, $nom, PREG_OFFSET_CAPTURE);
                preg_match("/(\/index)(.*)(\.html)/", $url, $id, PREG_OFFSET_CAPTURE);
                
                $urlXml = "http://tei.revues.org/".$nom[2][0]."-".$id[2][0].".xml";
            }
        }
        
       
        #ouvre le fichier via l'url et le copie dans un dossier
        $fich = fopen($urlXml, "r"); 
        $contents = ''; 
        if($fich) {
            while(!feof($fich)){ 
                 $contents .= fread($fich, 8192); 
            }
        }
        fclose($fich);
        
        $fich2 = fopen($dossier_fichier."fichier_a_annoter.xml", "w"); 
        fwrite($fich2, $contents); 
        fclose($fich2);
        
        #lance BILBO
        $saveRep = getcwd();
        
        chdir("code/bilbo");
        $newRep = getcwd();
        
        /*recupere les chemin sans bilbo*/
        $splitRep = split("/", $newRep);
        array_pop($splitRep);
        $newRepRes = join("/", $splitRep);
        $newRepRes .= "/fichierRes/";
        
        $res = exec("python ".$newRep."/src/mypkg/Main.py 1 ".$newRepRes." ".$newRepRes,$out,$error);
        $test = getcwd();
        chdir($saveRep);
        
        $fichier = $newRepRes."testEstCRF.xml";
        $resultat = file_get_contents($fichier);
        
        
        return $resultat;

    } 

    
    /*
     * Fonction getAnnotationTexte sert generer les annotations de la reference 
     * @param $reference  article à annoter
     * @return $result  article annoté
     */
    function getAnnotationBibliographieTexte($reference) {
        global $dossier_fichier_bilbo, $dossier_fichier;
        
        #supprime les fichiers du dossier buffer
        system("rm ".$dossier_fichier."*");
        
        #transforme la reference en xml pour l'analyser
        $resultat = transformeXml($reference, $dossier_fichier, "fichier_a_annoter.xml", "bibl");
        
        
        #lance BILBO
        $saveRep = getcwd();
        
        chdir("code/bilbo");
        $newRep = getcwd();
        
        /*recupere les chemin sans bilbo*/
        $splitRep = split("/", $newRep);
        array_pop($splitRep);
        $newRepRes = join("/", $splitRep);
        $newRepRes .= "/fichierRes/";

        $res = exec("python ".$newRep."/src/mypkg/Main.py 1 ".$newRepRes." ".$newRepRes,$out,$error);
        $test = getcwd();
        chdir($saveRep);
        
        $fichier = $newRepRes."testEstCRF.xml";
        $resultat = file_get_contents($fichier);
       

        return $resultat;
    } 
    
    /*
     * Fonction getAnnotationNoteTexte sert generer les annotations de la note 
     * @param $reference  article à annoter
     * @return $result  article annoté
     */
    function getAnnotationNoteTexte($reference) {
        global $dossier_fichier_bilbo, $dossier_fichier;
        
        #supprime les fichiers du dossier buffer
        system("rm ".$dossier_fichier."*");
        
        #transforme la reference en xml pour l'analyser
        $resultat = transformeXml($reference, $dossier_fichier, "fichier_a_annoter.xml", "note");
        
        
        #lance BILBO
        $saveRep = getcwd();
        
        chdir("code/bilbo");
        $newRep = getcwd();
        
        /*recupere les chemin sans bilbo*/
        $splitRep = split("/", $newRep);
        array_pop($splitRep);
        $newRepRes = join("/", $splitRep);
        $newRepRes .= "/fichierRes/";
        
        $res = exec("python ".$newRep."/src/mypkg/Main.py 2 ".$newRepRes." ".$newRepRes, $out, $error);
        $test = getcwd();
        chdir($saveRep);
        
        $fichier = $newRepRes."testEstCRF.xml";
        $resultat = file_get_contents($fichier);
        
        return $resultat;
    } 
    
            
/************************************ FONCTION COMPLEMENTAIRE *************************/
    /*/Applications/XAMPP/xamppfiles/htdocs/annotation/code
     * Fonction transformeXml permet de generer le fichier xml de la reference 
     * @param $reference  texte a transformer
     * @param $dossier  endroit ou creer le fichier xml ex : repertoire/dossier/
     * @param $nomFichier  nom du fichier xml que l'on va créer
     * @return $resultat
     */
    function transformeXml($reference, $dossier, $nomFichier, $balise) {
        $saveRep = getcwd();
        
        /*$splitRep = split("/", $saveRep);
        array_pop($splitRep);
        $rep = join("/", $splitRep);
        $rep .= "/fichierRes/";*/
        
        $resultat = $dossier.$nomFichier;
        
        $handle = fopen($dossier.$nomFichier, "w"); 
        if($balise == "bibl"){
            fwrite($handle, "<listBibl><bibl>".$reference."</bibl></listBibl>");
        }else{
            fwrite($handle, "<note place=\"foot\">".$reference."</note>"); 
        }
        fclose($handle);
        
        return $resultat;
    } 
    
    
/***************************** mise en place du service *****************************/
    // Désactivation du cache WSDL
    ini_set("soap.wsdl_cache_enabled", "0"); 
    ini_set("soap.wsdl_cache_ttl", "0");
    // Catch l'erreur si l'instanciation la classe Serveur
    // échoue, on retourne l'erreur
    try {
        $server = new SoapServer('config_wsdl2.wsdl');
        // On ajoute la méthode "getResult" que le serveur va gérer
        #  $server->setClass("Annotation");
        $server->addFunction("getAnnotationArticle");
        $server->addFunction("getAnnotationNoteArticle");
        $server->addFunction("getAnnotationBibliographieTexte");
        $server->addFunction("getAnnotationUrl");
        $server->addFunction("getAnnotationNoteTexte");

    } catch (Exception $e) {
        echo 'erreur'.$e;
    }
    
    // Si l'appel provient d'une requête POST (Web Service)
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        // On lance le serveur SOAP
        $server->handle();
    }
    else {
        echo '<strong>Ce web service contient les fonction suivante : </strong>';
        echo '<ul>';
        foreach($server -> getFunctions() as $func) {
            echo '<li>' , $func , '</li>';
        }
        echo '</ul>';
    }
    ?>