<?php
$data = array(
    'status' => "error",
    'msg' => '<div class="alert alert-danger">Something went wrong!</div>' 
);
$secret_key = "6LfYqRkUAAAAADABlTXuUfznWTpUx9aNV9bk1L_o";
if(isset($_POST['action']) && $_POST['action'] == "make_an_offer"){    
    // init error message 
	$errmsg= array();
	$captcha=$_POST['g-recaptcha-response'];
    $response=json_decode(file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".$secret_key."&response=".$captcha."&remoteip=".$_SERVER['REMOTE_ADDR']), true);
    /* Check required field not blank */	
	// Check if email has been entered and is valid	
    if (!$_POST['mao_name']) {
		$errmsg[] = '<p>Please enter your name</p>';
	}
	if (!$_POST['mao_radio']) {
		$errmsg[] = '<p>Please select Preferred contact</p>';
	}
    if (!$_POST['mao_email'] || !filter_var($_POST['mao_email'], FILTER_VALIDATE_EMAIL)) {
		$errmsg[] = '<p>Please enter a valid email address</p>';
	}	
	if (!$_POST['mao_phone']) {
		$errmsg[] = '<p>Please enter phone number</p>';
	}
	if (!$_POST['mao_price']) {
		$errmsg[] = '<p>Please enter offered price</p>';
	}
	if(!$captcha)
    {
         $errmsg[] .='<p>Please check the the captcha form</p>';
    }
    if($response['success'] == false)
    {
          $errmsg[] .='<p>Captcha is not verified. Please try again.</p>';
    }
	//Check if message has been entered
	if (!$_POST['mao_comments']) {
		$errmsg[] = '<p>Please enter your message</p>';
	}
    if(!empty($errmsg)){
        $result='';
    	$errors=implode(' ',$errmsg);
        $result='<div class="alert alert-danger"><p>Enter required fields..</p></div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );    
    } else {
        $name = $_POST['mao_name'];                 // Sender's name
		$preferred_contact = $_POST['mao_radio'];
    	$email = $_POST['mao_email'];     // Sender's email address
    	$phone  = $_POST['mao_phone'];     // Sender's email address
    	$price  = $_POST['mao_price'];     // Sender's website
    	$message = $_POST['mao_comments'];    // Sender's message
        $from = 'Demo Contact Form';    
    	$subject = 'Message from Contact Demo ';
    	$body = "From: $name \n";   
		$body = "Preferred Contact: $preferred_contact \n";   
      	$body.= "E-Mail: $email \n";
    	$body.= "Phone : $phone \n";  
    	$body.= "Price : $price \n";  
    	$body.= "Message : $message \n";
        if (mail ('salim.lunat@potenzaglobalsolutions.com', $subject, $body, $from)) {
			$result='<div class="alert alert-success">Thank you for contacting us. Your message has been successfully sent. We will contact you very soon!</div>'; 
		} 
		else {
            $result='<div class="alert alert-danger">Sorry there was an error sending your message. Please try again later.</div>';
		}
        $data = array(
            'status' => "success",
            'msg' => $result 
        );    	    
    }  
	header('Content-Type: application/json');
	echo json_encode($data);
    exit();   
} elseif(isset($_POST['action']) && $_POST['action'] == "request_more_info"){
	$errmsg= array();
	$showerrmsg= array();
	$captcha=$_POST['g-recaptcha-response'];
    $response=json_decode(file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".$secret_key."&response=".$captcha."&remoteip=".$_SERVER['REMOTE_ADDR']), true);
    if (!$_POST['rmi_name']) {
		$errmsg[] = '<p>Please enter your name</p>';
	}
    if (!$_POST['rmi_email']) {
		$errmsg[] = '<p>Please enter a valid email address</p>';
	}
    if (!filter_var($_POST['rmi_email'], FILTER_VALIDATE_EMAIL)) {
		$showerrmsg[] = '<p>Please enter a valid email address</p>';
	}
    if (!$_POST['rmi_phone']) {
		$errmsg[] = '<p>Please enter your Phone</p>';
	}	
	if (!$_POST['rmi_radio']) {
		$errmsg[] = '<p>Please select Preferred contact</p>';
	}
	
	if(!$captcha)
    {
         $errmsg[] .='<p>Please check the captcha form</p>';
    }
    if($response['success'] == false)
    {
          $showerrmsg[] .='<p>Captcha is not verified. Please try again.</p>';
    }
    if(!empty($errmsg)){
        $result='';
    	$errors=implode(' ',$errmsg);
        $result='<div class="alert alert-danger"><p>Enter Required fields..</p></div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );    
    }elseif(!empty($showerrmsg)){
		$result='';
    	$errors=implode(' ',$showerrmsg);
        $result='<div class="alert alert-danger">'.$errors.'</div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );  
	} else {
		$name = $_POST['rmi_name'];
		$optradio = $_POST['rmi_radio'];
		$emailid = $_POST['rmi_email'];
		$rmi_phone = $_POST['rmi_phone'];
        $rmi_message = $_POST['rmi_message'];
        $from = 'Demo Contact Form';    
    	$to = $emailid; 
    	$subject = 'Message from Contact Demo ';
    	$body = "From: $name \n";   
      	$body.= "E-Mail: $emailid \n";
        $body.= "E-Mail: $rmi_phone \n";
    	$body.= "Preferred Contact : $optradio \n";  
    	$body.= "Message : $rmi_message \n";
        if (mail ('salim.lunat@potenzaglobalsolutions.com', $subject, $body, $from)) {
			$result='<div class="alert alert-success">Thank you for contacting us. Your message has been successfully sent. We will contact you very soon!</div>'; 
		} 
		else {
            $result='<div class="alert alert-danger">Sorry there was an error sending your message. Please try again later.</div>';
		}
        $data = array(
            'status' => "success",
            'msg' => $result 
        );    	    
    }  
	header('Content-Type: application/json');
	echo json_encode($data);
    exit();  
} elseif(isset($_POST['action']) && $_POST['action'] == "schedule_test_drive"){
	$errmsg= array();
	$captcha=$_POST['g-recaptcha-response'];
	$response=json_decode(file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".$secret_key."&response=".$captcha."&remoteip=".$_SERVER['REMOTE_ADDR']), true);
    if (!$_POST['std_firstname']) {
		$errmsg[] = '<p>Please enter your name</p>';
	}
    if (!$_POST['std_email'] || !filter_var($_POST['std_email'], FILTER_VALIDATE_EMAIL)) {
		$errmsg[] = '<p>Please enter a valid email address</p>';
	}	
	if (!$_POST['std_optradio']) {
		$errmsg[] = '<p>Please select Preferred contact</p>';
	}
	if (!$_POST['std_phone']) {
		$errmsg[] = '<p>Please enter your phone number</p>';
	}
	if (!$_POST['std_day']) {
		$errmsg[] = '<p>Please enter your day of drive</p>';
	}
	if (!$_POST['std_time']) {
		$errmsg[] = '<p>Please enter your time of drive</p>';
	}
	if(!$captcha){
         $errmsg[] .='<p>Please check the the captcha form</p>';
    }
    if($response['success'] == false){
          $errmsg[] .='<p>Captcha is not verified. Please try again.</p>';
    }
    if(!empty($errmsg)){
        $result='';
    	$errors=implode(' ',$errmsg);
        $result='<div class="alert alert-danger"><p>Enter required fields..</p></div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );    
    } else {
		$name = $_POST['std_firstname'];
		$optradio = $_POST['std_optradio'];
		$email = $_POST['std_email'];   
		$phone  = $_POST['std_phone']; 
		$day  = $_POST['std_day'];  
		$time = $_POST['std_time']; 
        $from = 'Demo Contact Form';    
    	$subject = 'Message from Contact Demo ';
    	$body = "From: $name \n";   
		$body.= "Preferred Contact : $optradio \n";  
      	$body.= "E-Mail: $email \n";
    	$body.= "Phone : $phone \n";  
		$body.= "Day : $day \n";  
		$body.= "Time : $time \n";
        if (mail ('salim.lunat@potenzaglobalsolutions.com', $subject, $body, $from)) {
			$result='<div class="alert alert-success">Thank you for contacting us. Your message has been successfully sent. We will contact you very soon!</div>'; 
		} 
		else {
            $result='<div class="alert alert-danger">Sorry there was an error sending your message. Please try again later.</div>';
		}
        $data = array(
            'status' => "success",
            'msg' => $result 
        );    	    
    }  
	header('Content-Type: application/json');
	echo json_encode($data);
    exit();  
} elseif(isset($_POST['action']) && $_POST['action'] == "email_to_friend"){
	$errmsg= array();
	$captcha=$_POST['g-recaptcha-response'];
	$response=json_decode(file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".$secret_key."&response=".$captcha."&remoteip=".$_SERVER['REMOTE_ADDR']), true);
    if (!$_POST['etf_name']) {
		$errmsg[] = '<p>Please enter your name</p>';
	}
    if (!$_POST['etf_email'] || !filter_var($_POST['etf_email'], FILTER_VALIDATE_EMAIL)) {
		$errmsg[] = '<p>Please enter a valid email address</p>';
	}	
	if (!$_POST['etf_fmail']) {
		$errmsg[] = '<p>Please enter a valid friend email address</p>';
	}
	if (!$_POST['etf_fmessage']) {
		$errmsg[] = '<p>Please enter your message</p>';
	}
	if(!$captcha){
         $errmsg[] .='<p>Please check the the captcha form</p>';
    }
    if($response['success'] == false){
          $errmsg[] .='<p>Captcha is not verified. Please try again.</p>';
    }
    if(!empty($errmsg)){
        $result='';
    	$errors=implode(' ',$errmsg);
        $result='<div class="alert alert-danger"><p>Enter required fields..</p></div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );    
    } else {
		$name = $_POST['etf_name'];
		$email = $_POST['etf_email'];   
		$fmail  = $_POST['etf_fmail']; 
		$message  = $_POST['etf_fmessage'];
        $from = $email;    
    	$to = $fmail;
    	$subject = 'Message from Contact Demo ';
    	$body = "From: $name \n";   
      	$body.= "E-Mail: $email \n";
		$body.= "Friend E-Mail: $fmail \n";
		$body.= "Message : $message \n";
        if (mail ($to, $subject, $body, $from)) {
			$result='<div class="alert alert-success">Thank you for contacting us. Your message has been successfully sent. We will contact you very soon!</div>'; 
		} 
		else {
            $result='<div class="alert alert-danger">Sorry there was an error sending your message. Please try again later.</div>';
		}
        $data = array(
            'status' => "success",
            'msg' => $result 
        );    	    
    }  
	header('Content-Type: application/json');
	echo json_encode($data);
    exit();  
} elseif(isset($_POST['action']) && $_POST['action'] == "trade_in_appraisal"){
	$errmsg = array();
	$captcha = $_POST['g-recaptcha-response'];
	$response=json_decode(file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".$secret_key."&response=".$captcha."&remoteip=".$_SERVER['REMOTE_ADDR']), true);
    if (!$_POST['tia_firstname']) {
		$errmsg[] = '<p>Please enter your First name</p>';
	}
    if (!$_POST['tia_lastname']) {
		$errmsg[] = '<p>Please enter your Last Name</p>';
	}
	
	if (!$_POST['tia_phone']) {
		$errmsg[] = '<p>Please enter your Phone</p>';
	}
	if (empty($_POST['tia_email']) || !filter_var($_POST['tia_email'], FILTER_VALIDATE_EMAIL)) {
		$errmsg[] = '<p>Please enter a valid email address</p>';
	}	
	if (!$_POST['tia_optradio']) {
		$errmsg[] = '<p>Please select preferred contact</p>';
	}
	if (!$_POST['tia_comments']) {
		$errmsg[] = '<p>Please enter comments</p>';
	}
	if (!$_POST['tia_year']) {
		$errmsg[] = '<p>Please enter year</p>';
	}
	if (!$_POST['tia_make']) {
		$errmsg[] = '<p>Please enter make</p>';
	}
	if (!$_POST['tia_model']) {
		$errmsg[] = 'Please enter model</p>';
	}
	if (!$_POST['tia_colour']) {
		$errmsg[] = '<p>Please enter colour</p>';
	}
	if (!$_POST['tia_vin']) {
		$errmsg[] = '<p>Please enter vin</p>';
	}
	if (!$_POST['tia_kilometers']) {
		$errmsg[] = '<p>Please enter kilometers</p>';
	}
	if (!$_POST['tia_engine']) {
		$errmsg[] = '<p>Please enter engine</p>';
	}
	if(!$captcha)
    {
         $errmsg[] .='<p>Please check the the captcha form</p>';
    }
    if($response['success'] == false)
    {
          $errmsg[] .='<p>Captcha is not verified. Please try again.</p>';
    }
    if(!empty($errmsg)){
        $result='';
    	$errors=implode(' ',$errmsg);
        $result='<div class="alert alert-danger"><p>Enter required fields..</p></div>';
        $data = array(
            'status' => "error",
            'msg' => $result 
        );    
    } else {
		$firstname = (isset($_POST['tia_firstname']))?$_POST['tia_firstname']:'';
		$lastname = (isset($_POST['tia_lastname']))?$_POST['tia_lastname']:'';;   
		$workphone  = (isset($_POST['tia_workphone']))?$_POST['tia_workphone']:''; 
		$phone  = (isset($_POST['tia_phone']))?$_POST['tia_phone']:'';
		$email = (isset($_POST['tia_email']))?$_POST['tia_email']:'';
		$preferredcontact = (isset($_POST['tia_optradio']))?$_POST['tia_optradio']:'';   
		$comments  = (isset($_POST['tia_comments']))?$_POST['tia_comments']:''; 
		$options  = (isset($_POST['tia_options'])) ? $_POST['tia_options'] : "";
		$year = (isset($_POST['tia_year']))?$_POST['tia_year']:'';
		$make = (isset($_POST['tia_make']))?$_POST['tia_make']:'';   
		$model  = (isset($_POST['tia_model']))?$_POST['tia_model']:''; 
		$exterior_color = (isset($_POST['tia_colour']))?$_POST['tia_colour']:'';
		$vin = (isset($_POST['tia_vin']))?$_POST['tia_vin']:'';
		$kilometers = (isset($_POST['tia_kilometers']))?$_POST['tia_kilometers']:'';
		$engine = (isset($_POST['tia_engine']))?$_POST['tia_engine']:'';
		$doors = (isset($_POST['tia_doors']))?$_POST['tia_doors']:'';
		$transmission = (isset($_POST['tia_transmission']))?$_POST['tia_transmission']:'';
		$drivetrain = (isset($_POST['tia_drivetrain']))?$_POST['tia_drivetrain']:'';
		$ratingbody  = (isset($_POST['tia_vehicle_rating_body']))?$_POST['tia_vehicle_rating_body']:'';
		$tires = (isset($_POST['tia_vehicle_rating_tires']))?$_POST['tia_vehicle_rating_tires']:'';
		$enginecondition = (isset($_POST['tia_vehicle_rating_engine']))?$_POST['tia_vehicle_rating_engine']:'';   
		$clutch  = (isset($_POST['tia_vehicle_rating_clutch']))?$_POST['tia_vehicle_rating_clutch']:''; 
		$glass  = (isset($_POST['tia_vehicle_rating_glass']))?$_POST['tia_vehicle_rating_glass']:'';
		$interior = (isset($_POST['tia_vehicle_rating_interior']))?$_POST['tia_vehicle_rating_interior']:'';
		$exhaust = (isset($_POST['tia_vehicle_rating_exhaust']))?$_POST['tia_vehicle_rating_exhaust']:'';   
		$vehical_info_1  = (isset($_POST['tia_vehical_info_1']))?$_POST['tia_vehical_info_1']:''; 
		$vehical_info_2  = (isset($_POST['tia_vehical_info_2']))?$_POST['tia_vehical_info_2']:'';
		$vehical_info_3  = (isset($_POST['tia_vehical_info_3']))?$_POST['tia_vehical_info_3']:'';
		$title_history_1 = (isset($_POST['tia_lineholder_email']))?$_POST['tia_lineholder_email']:'';   
		$title_history_2  = (isset($_POST['tia_titleholder_email']))?$_POST['tia_titleholder_email']:''; 
		$vehical_assessment_1  = (isset($_POST['tia_textarea_1']))?$_POST['tia_textarea_1']:'';
		$vehical_assessment_2  = (isset($_POST['tia_textarea_2']))?$_POST['tia_textarea_2']:'';
		$vehical_assessment_3  = (isset($_POST['tia_textarea_3']))?$_POST['tia_textarea_3']:'';
		$vehical_assessment_4  = (isset($_POST['tia_textarea_4']))?$_POST['tia_textarea_4']:'';
		$vehical_assessment_5  = (isset($_POST['tia_textarea_5']))?$_POST['tia_textarea_5']:'';
		$vehical_assessment_6  = (isset($_POST['tia_textarea_6']))?$_POST['tia_textarea_6']:'';
        $from = $firstname." ".$lastname;    
    	$to = $email;
    	$subject = 'Message from Contact Demo ';
    	$body = "From : $firstname $lastname \n"; 
		$body.= "WorkPhone : $workphone \n";
		$body.= "Phone : $phone \n";		
      	$body.= "E-Mail : $email \n";
		$body.= "Preferred Contact : $preferredcontact \n";
		$body.= "Comments : $comments \n";
		if(isset($options)&&!empty($options)){
			foreach($options as $option){
				$body.= "Options : $option \n";
			}
		}else{
			$body.= "Options : \n";
		}
		$body.= "Year : $year \n";
		$body.= "Make : $make \n";
		$body.= "Model : $model \n";
		$body.= "Exterior Color : $exterior_color \n";
		$body.= "VIN : $vin \n";
		$body.= "Kilometers : $kilometers \n";
		$body.= "Engine : $engine \n";
		$body.= "Doors : $doors \n";
		$body.= "Transmission : $transmission \n";
		$body.= "Drivetrain : $drivetrain \n";
		$body.= "Body (dents, dings, rust, rot, damage) : $ratingbody \n";
		$body.= "Tires (tread wear, mismatched) : $tires \n";
		$body.= "Engine (running condition, burns oil, knocking) : $enginecondition \n";
		$body.= "Transmission / Clutch (slipping, hard shift, grinds) : $clutch \n";
		$body.= "Glass (chips, scratches, cracks, pitted) : $glass \n";
		$body.= "Interior (rips, tears, burns, faded/worn) : $interior \n";
		$body.= "Exhaust (rusted, leaking, noisy) : $exhaust \n";
		$body.= "Was it ever a lease or rental return? : $vehical_info_1 \n";
		$body.= "Is the odometer operational and accurate? : $vehical_info_2 \n";
		$body.= "Detailed service records available? : $vehical_info_3 \n";
		$body.= "Is there a lienholder? : $title_history_1 \n";
		$body.= "Who holds this title? : $title_history_2 \n";
		$body.= "Does all equipment and accessories work correctly? : $vehical_assessment_1 \n";
		$body.= "Did you buy the vehicle new? : $vehical_assessment_2 \n";
		$body.= "Has the vehicle ever been in any accidents? : $vehical_assessment_3 \n";
		$body.= "Is there existing damage on the vehicle? Where? : $vehical_assessment_4 \n";
		$body.= "Has the vehicle ever had paint work performed? : $vehical_assessment_5 \n";
		$body.= "Is the title designated 'Salvage' or 'Reconstructed'? : $vehical_assessment_6 \n";        
        
        if (mail ('salim.lunat@potenzaglobalsolutions.com', $subject, $body, $from)) {
			$result='<div class="alert alert-success">Thank you for contacting us. Your message has been successfully sent. We will contact you very soon!</div>'; 
		} 
		else {
            $result='<div class="alert alert-danger">Sorry there was an error sending your message. Please try again later.</div>';
		}        
        
        $data = array(
            'status' => "success",
            'msg' => $result 
        );    	    
    }  
	header('Content-Type: application/json');
	echo json_encode($data);
    exit();  
}
echo json_encode($data); 
?>