const { error } = require("jquery");

$('.nav-tabs a').on('shown.bs.tab', function (e) {
    alert('hii there')
    var current_tab = e.target;
    var previous_tab = e.relatedTarget;    
});


// Save Employee Master details
function saveEmpData() {
    var EmpData = '';
    var EmployeeID = $.trim($("#txtEmpId").val());
    var FirstName = $.trim($("#txtFirstName").val());
    var MiddleName = $.trim($("#txtMiddleName").val());
    var LastName = $.trim($("#txtLastName").val());
    var FathersName = $.trim($("#txtFatherName").val());
    var MonileNo1 = $.trim($("#txtMobileNo1").val());
    var MobileNo2 = $.trim($("#txtMobile2").val());
    var EmailId = $.trim($("#txtMailID").val());
    var Gender = $("#Gender").val(); 
    var MaritalStatusID = $("#MaritalStatusID").val();
    var DOB = $("#DOBdatepicker").val();
    var DOJ = $("#DOJdatepicker").val();
    var DOL = $("#DOLdatepicker").val();
    var CAddress1 = $("#txtCAddress1").val();
    var CAddress2 = $("#txtCAddress2").val();
    var CAddress3 = $("#txtCAddress3").val();
    var CState = $("#txtCState").val();
    var CCountry = $("#txtCCountry").val();
    var CPincode = $("#txtCPincode").val();
    var PAddress1 = $("#txtPAddress1").val();
    var PAddress2 = $("#txtPAddress2").val();
    var PAddress3 = $("#txtPAddress3").val();
    var PState = $("#txtPState").val();
    var PCountry = $("#txtPCountry").val();
    var PPincode = $("#txtPPIN").val();
    if (FirstName == null || FirstName == "") {
        yToastr.Error("Please Enter the  Employee FirstName", toastr.options.positionClass = "toast-bottom-right");
        return false;
    }
    if (FathersName == null || FathersName == "") {
        yToastr.Error("Please Enter the  Employee Father's Name");
        return false;
    }
    if (MonileNo1 == null || MonileNo1 == "") {
        yToastr.Error("Please Enter the  Employee Mobile Number");
        return false;
    }
    if (Gender == 'Select Gender' || Gender == "" || Gender == null) {
        yToastr.Error("Please Enter the  Gender");
        return false;
    }
    if (DOB == null || DOB == "") {
        yToastr.Error("Please Enter Employee Date Of Birth");
        return false;
    }
    if (DOJ == null || DOJ == "") {
        yToastr.Error("Please Enter Date Of Joining");
        return false;
    }
    if (PAddress1 == null || PAddress1 == "") {
        yToastr.Error("Please Enter Employee Permanent Address3");
        return false;
    }
    if (PAddress2 == null || PAddress2 == "") {
        yToastr.Error("Please Enter Employee Permanent Address2");
        return false;
    }
    if (PAddress3 == null || PAddress3 == "") {
        yToastr.Error("Please Enter Employee Permanent Address3");
        return false;
    }
    if (PState == null || PState == "") {
        yToastr.Error("Please Enter Employee Permanent PState");
        return false;
    }
    if (PCountry == null || PCountry == "") {
        yToastr.Error("Please Enter Employee Permanent PCountry");
        return false;
    }
    if (PPincode == null || PPincode == "") {
        yToastr.Error("Please Enter Employee Permanent PPincode");
        return false;
    }

    EmpData = {
        EmployeeID: EmployeeID,
        FirstName: FirstName,
        MiddleName: MiddleName,
        LastName: LastName,
        FathersName: FathersName,
        MobileNumber1: MonileNo1,
        MobileNumber2: MobileNo2,
        MailID: EmailId,
        Gender: Gender,
        MaritalStatusID: MaritalStatusID,
        DateOfBirth: DOB,
        DateOfJoining: DOJ,
        DateOfLeaving: DOL,
        PermanantAddress1: PAddress1,
        PermanantAddress2: PAddress2,
        PermanantAddress3: PAddress3,
        PermanantState: PState,
        PermanantCountry: PCountry,
        PermanantPinCode: PPincode,
        CommunicationAddress1: CAddress1,
        CommunicationAddress2: CAddress2,
        CommunicationAddress3: CAddress3,
        CommunicationState: CState,
        CommunicationCountry: CCountry,
        CommunicationPinCode: CPincode
    }

    $.ajax({
        url: 'Transaction/SaveEmployeeDetails',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(EmpData),
        success: function (response) {            
            if (response != null && response.success) {
                var EmpId = response.data;               
                yToastr.Success('Employee Data Updated Successfully, EmpID -' + EmpId);
            } else {
                yToastr.Success(response.responseText);
            }

        },
        error: function (response) {           
            yToastr.Error(response.responseText);
        }
    });
}

function UsePermanentAddress() {
    if ($("input[name='chkUsePaddress']:checked").prop('checked') == true) {
        $("#txtCAddress1").val($("#txtPAddress1").val());
        $("#txtCAddress2").val($("#txtPAddress2").val());
        $("#txtCAddress3").val($("#txtPAddress3").val());
        $("#txtCState").val($("#txtPState").val());
        $("#txtCCountry").val($("#txtPCountry").val());
        $("#txtCPincode").val($("#txtPPIN").val());
    }
    else {
        $("#txtCAddress1").val('');
        $("#txtCAddress2").val('');
        $("#txtCAddress3").val('');
        $("#txtCState").val('');
        $("#txtCCountry").val('');
        $("#txtCPincode").val('');
    }
    
}
function saveLegalData() {

    var EmpLegalData = '';
    var EmployeeID = $.trim($("#txtEmpId").val());
    var AadharNumber = $.trim($("#txtAadhar").val());
    var PANNumber = $.trim($("#txtPANNo").val());
    var PFNumber = $.trim($("#txtPF").val());
    var PFUANumber = $.trim($("#txtPFUAN").val());
    var ESICCodeNumber = $.trim($("#txtESICCode").val());
    var BankaccountNumber = $.trim($("#txtBankAccountNo").val());
    var BankName = $.trim($("#txtBankName").val());
    var IFSCCodeNumber = $.trim($("#txtIFSCCode").val());
    var Nationality = $.trim($("#txtNationality").val());

    if (AadharNumber == null || AadharNumber == "") {
        yToastr.Error("Please Enter the AadharNumber", toastr.options.positionClass = "toast-bottom-right");
        return false;
    }
    if (PANNumber == null || PANNumber == "") {
        yToastr.Error("Please Enter the PANNumber");
        return false;
    }
    if (BankaccountNumber == null || BankaccountNumber == "") {
        yToastr.Error("Please Enter  BankaccountNumber");
        return false;
    }
    if (BankName == null || BankName == "") {
        yToastr.Error("Please Enter BankName");
        return false;
    }
    if (IFSCCodeNumber == null || IFSCCodeNumber == "") {
        yToastr.Error("Please Enter IFSCCode");
        return false;
    }
    if (Nationality == null || Nationality == "") {
        yToastr.Error("Please Enter  Nationality");
        return false;
    }

    var isValid = isValidAadhaarNumber(AadharNumber);
    if (isValid == false) {
        yToastr.Error("Enter Valid Aadhar Number");
        return false;
    }
    var isValid = isValidPANNumber(PANNumber);
    if (isValid == false) {
        yToastr.Error("Enter Valid PANNumber");
        return false;
    }
  
    
    EmpLegalData = {
        EmployeeID: 'ABC102',
        AadharNumber: AadharNumber,
        PANNumber: PANNumber,
        PFNumber: PFNumber,
        PFUANumber: PFUANumber,
        ESICCodeNumber: ESICCodeNumber,
        BankAccountNumber: BankaccountNumber,
        BankName: BankName,
        IFSCCodeNumber: IFSCCodeNumber,
        Nationality: Nationality
    }    
    $.ajax({
        url: 'Transaction/saveEmployeeLegelDetails',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(EmpLegalData),
        success: function (response) {
            if (response != null && response.success) {            
                yToastr.Success('Legal Data Updated Successfully!');
                clearLegalData();
            } else {
                yToastr.Success(response.responseText);
            }

        },
        error: function (response) {
            yToastr.Error(response.responseText);
        }
    });

}
function isValidAadhaarNumber(AadharNumber) {           
        let regex = new RegExp(/^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$/);
        // Return true if the aadhaar_number matched the ReGex
        if (regex.test(AadharNumber) == true) {
            return true;
        }
        else {
            return false;
        }
}
function isValidPANNumber(PANNumber) {
    let regex = new RegExp(/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/);       
    if (regex.test(PANNumber) == true) {
        return true;
    }
    else {
        return false;
    }
}

function clearLegalData() {
    $("#txtAadhar").val('');
    $("#txtPANNo").val('');
    $("#txtPF").val('');
    $("#txtPFUAN").val('');
    $("#txESICCode").val('');
    $("#txtBankAccountNo").val('');
    $("#txtBankName").val('');
    $("#txtIFSCCode").val('');
    $("#txtNationality").val('');
 
}

let myTable = document.getElementById('tblEmpFamily');
let totalRowCount = myTable.rows.length;
$('#dynamic_form').on('submit', function (event) {
    event.preventDefault();
    var bool = validatedata();
    var AllFamilyData = [];
    for (var i = 1; i <= totalRowCount; i++) {
        var FamilyDetails = {
            FFirstName: $.trim($("#txtFirstName" + i).val()),
            FLastName: $.trim($("#txtLastName" + i).val()),
            FSex: $.trim($("#txtLastName" + i).val()),
            FRelationship: $.trim($("#txtRelationship" + i).val()),
            FAadharNo: $.trim($("#txtAadhar" + i).val())
        }
        AllFamilyData.push(FamilyDetails);
    }

    //$.ajax({
    //    url: 'Transaction/SaveFamilyDetails',
    //    type: 'POST',
    //    contentType: 'application/json',
    //    dataType: 'json',
    //    data: $(this).serialize(),
    //    success: function (data) {
    //        if (data.error) {
    //            alert(data.error[0])
    //        } else {
    //            alert(data);
    //        }

    //    },
    //    error: function (response) {
    //        yToastr.Error(response.responseText);
    //    }
    //});
})


function validatedata() {
    debugger;
    // var data = $("#dynamic_form").serialize();
    var data = $("#dynamic_form").serializeArray();
    var data_array = data;
    for (var i = 1; i <= totalRowCount; i++) {
        var FFirstName = $.trim($("#txtFFirstName" + i).val());
        var FLastName = $.trim($("#txtFLastName" + i).val());
        var FSex = $.trim($("#ddlFGender" + i).val());
        var FRelationship = $.trim($("#ddlFReleationship" + i).val());
        var FAadharNo = $.trim($("#txtFamilyAadhar" + i).val());
        var FDOB = $.trim($("#txtFamilydob" + i).val());

        if (FFirstName == '' || FFirstName == null || FLastName == '' || FLastName == null || FLastName == null || FSex == '' || FSex == null || FRelationship == '' || FRelationship == null || FAadharNo == '' || FAadharNo == null || FDOB == '' || FDOB == null) {
            yToastr.Error("Enter all the fields");
            return false;
        }
    }

    return indexed_array;
}

