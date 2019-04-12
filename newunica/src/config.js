window.appUrl = '';
window.adminUrl = '';

window.showError = (text) => {
  swal({
    title: "Error",
    text: text,
    icon: "error",
    button: "Okay",
  });
}
window.showWarning = (text) => {
  swal({
    title: "Warning",
    text: text,
    icon: "warning",
    button: "Okay",
  });
}
window.showInfo = (text) => {
  swal({
    title: "Information",
    text: text,
    icon: "info",
    button: "Okay",
  });
}
window.showSuccess = (title, text, button) => {
  swal({
    title: title,
    text: text,
    icon: "success",
    button: "Okay",
  });
}

//Global Confirmation Dialog
window.globalConfirmationDialog = (inputTitle, inputText, successCallback, cancelCallback) => {
  swal({
    title: inputTitle,
    text: inputText,
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        successCallback()
      } else {
        if (cancelCallback != null) {
          cancelCallback();
        }
      }
    });
}
