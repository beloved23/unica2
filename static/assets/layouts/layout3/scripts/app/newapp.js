//Vue.component('input-tag', InputTag);
// Vue.http.headers.common['Content-Type'] = 'application/x-www-form-urlencoded';

new Vue({
    delimiters: ['[[', ']]'],
        el: '#travel-form-first',
        data: {
            purpose: '',
            checked: '',
            tagsArray:[],
            group:{},
            groups: [],
            submitted:false,
            loading: false,
            showTable:false
        },
        methods: {
            addAuuid: function(){
                this.loading = true
                if (this.group.auuid == undefined){
                    swal({
                        title: "Error",
                        text: "Please add auuid",
                        icon: "error",
                        button: "Okay",
                      });
                      this.loading = false
                }else{
                    console.log('hello', this.group.auuid)
                    //this.$http.post('/travel/emails/', {'auuid': this.group.auuid })//, { headers : { 'Content-Type': 'application/x-www-form-urlencoded' }})
                    //axios.post('/travel/emails/', {auuid : '2330854'})//, { headers : { 'Content-Type': 'application/x-www-form-urlencoded' }})
                    axios({
                        method: 'post',
                        url: '/travel/emails/',
                        //**withCredentials: true,**
                        data: {
                          "auuid": this.group.auuid
                        },
                        headers: {
                          "Content-Type": "application/x-www-form-urlencoded",
                          "Cache-Control": "no-cache"
                        }
                      })
                    .then((response) => {
                        this.loading = false;
                        console.log(response.data.isFound)
                        if(response.data.isFound)
                        {
                            console.log(response.data)
                            this.group.email = 'adegoke';
                            this.group.name = 'femi';
                            this.groups.push(this.group);
                            this.group = {}

                        }else{
                            swal({
                                title: "Error",
                                text: "Auuid not found",
                                icon: "error",
                                button: "Okay",
                              });
                        }
                        })
                        .catch((err) => {
                            swal({
                                title: "Error",
                                text: "An error occured",
                                icon: "error",
                                button: "Okay",
                              });
                            console.log(err);
                            this.loading = false
                        })
                }

        },
        removeAuuid: function(index){
            //this.loading = false
            this.groups.splice(index, 1);
        }
        }
        });
