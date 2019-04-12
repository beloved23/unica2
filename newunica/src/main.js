import Vue from 'vue'
//import App from './App.vue'
import swal from 'sweetalert';
import axios from 'axios';
require('./config')
require('jquery-validation');
require('jquery')

//import vueDropzone from "vue2-dropzone";
//
//
//new Vue({
// delimiters: ['[[', ']]'],
//  el :'#dropzone',
//  data: () => ({
//    dropOptions: {
//      url: "/campaign/import/",
//      maxFileSize: 100, // MB
//      maxFiles: 4,
//      chunking: true,
//      chunkSize: 500, // Bytes
//      thumbnailWidth: 150, // px
//      thumbnailHeight: 150,
//      addRemoveLinks: true
//    }
//  }),
//  components: {
//    vueDropzone
//  },
//   methods: {
//      afterComplete(file, response) {
//      $('#name_id').val(response.Message);
//    }
//    }
//});


new Vue({
    delimiters: ['[[', ']]'],
        el: '#travel-form-first',
        data: {
            base_file: '',
            broadcast_name: '',
            message: '',
            broadcast_description:'',
            sender: '',
            checked: '',
            schedule_start: '',
            content_type:'',
            end_time : '',
            user: postdetails,
            submitted:false,
            loading: false,
            showTable:false
        },
        mounted (){
         this.validateForm();
        },
        methods: {
         validateForm: function(){
         let parent = this;
            //event.preventDefault();
            $('#travelForm').validate({
            submitHandler: function(form) {
            parent.submitUploadForm();
            }
           });
            },
         submitUploadForm: function(){
            axios({
                  method: 'post',
                  url: '/campaign/target/',
                  //**withCredentials: true,**
                  data: {
                    broadcast_name: this.broadcast_name,
                    broadcast_description: this.broadcast_description,
                    sender: this.sender,
                    message: this.message,
                    base_file : this.base_file,
                    schedule_start :this.schedule_start,
                    content_type: this.content_type,
                    end_time: this.end_time,
                    user: this.user
                  },
                  headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    //"Cache-Control": "no-cache"
                  }
                }).then((response) => {
                  this.loading = false;
                  if(response.data.action){
                    showSuccess(response.data.message);
                    //window.location = "/travel/create/"+ response.data.pk;
                  }else{
                    showError("An error occured! Please try again later");
                  }
                  }
                  )
                  .catch((err) => {
                      showError("An error occured, please try again later");
                      console.log(err);
                      this.loading = false;
                  })
         }
        }


     });




new Vue({
    delimiters: ['[[', ']]'],
    el: '#Details',
    data:{
        deleteMe:'Thanksme',
    },
    methods:{
        deleteTravel:function(id){
            swal({
            title: 'Delete',
            text: 'Delete travel request',
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
          if (willDelete) {
              //console.log(id);
            window.location =('/travel/delete/'+ id);
          }
        });
        }
    }
});


new Vue({
  delimiters: ['[[', ']]'],
  el:'#actions',
  data:{
    delagate:''
  }


});
