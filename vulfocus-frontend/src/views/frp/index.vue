<template>
  <div class="app-container">
    <el-tabs style="margin-left: 20px">
      <el-tab-pane label="FRP设置">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form label-width="170px" style="margin-top: 30px" v-loading="loading" :model="data" element-loading-text="修改中">
              <el-form-item label="是否启用FRP">
                <el-col :span="20">
                  <el-switch v-model="data.switch" on-value=true off-value=false></el-switch>
                </el-col>
              </el-form-item>
              <el-form-item label="Frp服务端地址">
                <el-col :span="20">
                  <el-input v-model="data.frp_url"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="域名设置">
                <el-col :span="20">
                  <el-input v-model="data.domain" placeholder="请输入内容"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="FRP模板">
                <el-col :span="20">
                  <el-input type="textarea" autosize v-model="data.frp_template"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="settingUpdate">修改</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="FRP映射">
          <el-table :data="frpdata" border stripe align = "center" style="width: 100%" v-loading="tabLoading">
            <el-table-column type="index" width="30"> </el-table-column>
            <el-table-column prop="frpid" label="FRPID" width="290"></el-table-column>
            <el-table-column prop="frp_subdomain" label="访问子域名" width="270"></el-table-column>
            <el-table-column prop="dockerid" label="容器ID" width="150" min-width="270"></el-table-column>
            <el-table-column prop="container_status" label="容器状态" width="80"></el-table-column>
            <el-table-column prop="container_port" label="容器端口" width="80"> </el-table-column>
            <el-table-column prop="frpconfig" label="FRP配置"> </el-table-column>
            <el-table-column prop="frpconfig" label="操作" width="200">
              <template slot-scope="{row}">
                <el-button size="mini" type="primary" icon="el-icon-edit" @click="deleteFrp(row)" >删除</el-button>
              </template>
            </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>

  import { frpSettings, settingUpdate, deleteFrpc } from "@/api/frp"
  export default {
  data() {
    return {
      data: {
        domain: "",
        frp_template: "",
        switch: false,
        frp_url: "",
      },
      frpdata: [],
      loading: false,
      tabLoading: true,
    }
  },
  created() {
    this.initSetting()
  },
  methods: {
    initSetting() {
      frpSettings().then(response => {
        let rspData = response.data
        if(rspData.status === 200){
          this.data = rspData.data.config
          this.frpdata = rspData.data.all
          this.tabLoading = false
        }else{
          for(let i; i < rspData.msg.length; i++){
            this.$message({
              message: rspData.msg[i],
              type: "info",
            })
          }
        }
      })
    },
    settingUpdate() {
      let formData = new FormData()
      formData.set("domain", this.data.domain)
      formData.set("frp_template", this.data.frp_template)
      formData.set("switch", this.data.switch)
      formData.set("frp_url", this.data.frp_url)
      this.loading = true
      settingUpdate(formData).then(response => {
        let rspData = response.data
        this.loading = false
        if(rspData.status === 200){
          this.data = rspData.data
          this.$message({
            message: '修改成功',
            type: "success",
          })
        }else{
          this.$message({
            message: rspData.msg,
            type: "error",
          })
        }
      })
    },
    deleteFrp(row) {
      let formData = new FormData()
      formData.set("frpid", row.frpid)
      this.loading = true
      deleteFrpc(formData).then(response => {
        let rspData = response.data
        this.loading = false
        if (rspData.status === 200) {
          this.data = rspData.data
          this.$message({
            message: '删除成功',
            type: "success",
          })
        } else {
          this.$message({
            message: rspData.msg,
            type: "error",
          })
        }
      })
    },
  }
}

</script>

<style lang="scss">
  .avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 330px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 330px;
  height: 178px;
  display: block;
}

.el-table .cell {
  white-space: pre-line;
}
</style>

<style scoped>
.relationContainer{
  display:flex;
  justify-content:center;/*主轴上居中*/
  align-items:flex-end;/*侧轴上居中*/

}
</style>
