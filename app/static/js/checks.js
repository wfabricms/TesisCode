
function onCheck1() {
    check1 = document.getElementById("check1")
    check2 = document.getElementById("check2")
    check3 = document.getElementById("check3")
    check4 = document.getElementById("check4")
    check5 = document.getElementById("check5")
    if (check1.checked) {
        check2.checked = false;
        check3.checked = false;
        check4.checked = false;
        check5.checked = false;
    }
    else{
        check2.checked = false;
        check3.checked = false;
        check4.checked = false;
        check5.checked = false;
    }
  }
  function onCheck2() {
    check1 = document.getElementById("check1")
    check2 = document.getElementById("check2")
    check3 = document.getElementById("check3")
    check4 = document.getElementById("check4")
    check5 = document.getElementById("check5")

    if (check2.checked) {
        check1.checked = true;
        check3.checked = false;
        check4.checked = false;
        check5.checked = false;
    }
    else{
        check1.checked = true;
        check3.checked = false;
        check4.checked = false;
        check5.checked = false;
    }
}
    
function onCheck3() {
    check1 = document.getElementById("check1")
    check2 = document.getElementById("check2")
    check3 = document.getElementById("check3")
    check4 = document.getElementById("check4")
    check5 = document.getElementById("check5")
    if (check3.checked) {

        check1.checked = true;
        check2.checked = true;
        check4.checked = false;
        check5.checked = false;
    }
    else{
        check1.checked = true;
        check2.checked = true;
        check4.checked = false;
        check5.checked = false;
    }
}
   
function onCheck4() {
    check1 = document.getElementById("check1")
    check2 = document.getElementById("check2")
    check3 = document.getElementById("check3")
    check4 = document.getElementById("check4")
    check5 = document.getElementById("check5")
    if (check4.checked) {
        check1.checked = true;
        check2.checked = true;
        check3.checked = true;
        check5.checked = false;
    }
    else{
        check1.checked = true;
        check2.checked = true;
        check3.checked = true;
        check5.checked = false;
    }
}
   
function onCheck5() {
    check1 = document.getElementById("check1")
    check2 = document.getElementById("check2")
    check3 = document.getElementById("check3")
    check4 = document.getElementById("check4")
    check5 = document.getElementById("check5")
    if (check5.checked) {
        check1.checked = true;
        check2.checked = true;
        check3.checked = true;
        check4.checked = true;
    }
}