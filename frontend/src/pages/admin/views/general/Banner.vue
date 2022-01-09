<template>
    <div class="view">
        <Panel title="Current Images">
          <div class="banner-images">
            <div
              v-for="(image, index) in bannerImageList"
              :key="index"
            >
              <b-img
                :src=image.path
                rounded
                class="banner-preview"
              />
            </div>
          </div>
            <b-table
                style="margin-top: 20px;"
                :items="bannerImageList"
                :fields="bannerImageListFields"
            >
              <template #cell(id)="data">
                {{ data.index + 1 }}
              </template>
              <template #cell(visible)="data">
                <b-form-checkbox v-model="data.item.visible" switch @change="handleVisibleSwitch(data.item)"/>
              </template>
              <template #cell(options)="data">
                <icon-btn
                  name="Delete"
                  icon="trash"
                  @click.native="deleteImage(data.item.id)"
                />
              </template>
            </b-table>
        </Panel>
        <Panel title="Import New Image">
            <div>* Banner image size: 2000 * 613</div>
            <b-form-file
                v-model="newImage"
                accept="image/*"
                style="margin-top: 10px;"
                @input="uploadImage"
                ref="image-input"
                id = "imageUpload"
            >
            </b-form-file>
            <b-button
                variant="primary"
                size="md"
                style="margin-top: 10px;"
                @click="insertImage"
                :disabled="disableAddButton"
            >Add</b-button>
        </Panel>
    </div>
</template>

<script>
import api from '../../api.js'
import time from '@/utils/time'

export default {
  name: 'Banner',
  data () {
    return {
      bannerImageList: [],
      bannerImageListFields: [
        { key: 'id', label: '#' },
        { key: 'title', label: 'Title' },
        {
          key: 'create_time',
          label: 'Create Time',
          formatter: value => {
            return time.utcToLocal(value, 'YYYY-M-DD HH:mm')
          }
        },
        { key: 'visible', label: 'Visible' },
        { key: 'options', label: 'Options' }
      ],
      newImage: {
        img_name: '',
        img_path: ''
      },
      disableAddButton: true
    }
  },
  async mounted () {
    const res = await api.getBannerImage()
    this.bannerImageList = res.data.data
  },
  methods: {
    async insertImage () {
      this.$refs['image-input'].reset()
      const data = {
        title: this.newImage.img_name,
        path: this.newImage.img_path
      }
      await api.createBannerImage(data)
      const res = await api.getBannerImage()
      this.bannerImageList = res.data.data
      this.disableAddButton = true
    },
    async uploadImage () {
      const self = this
      const imageUpload = document.getElementById('imageUpload')
      if (typeof (imageUpload.files) === 'undefined') {
        return
      }
      const reader = new FileReader()
      reader.readAsDataURL(imageUpload.files[0])
      reader.onload = function (e) {
        const image = new Image()
        image.src = e.target.result
        image.onload = async function () {
          const imgheight = this.height
          const imgwidth = this.width
          if (imgheight !== 613 || imgwidth !== 2000) {
            self.$confirm('Please check size of image. \nThe size of banner image should be 2000*613.', 'Check size of image', 'warning', false)
            self.$refs['image-input'].reset()
            return
          }
          const formData = new FormData()
          formData.append('image', self.newImage)
          if (self.newImage === null) {
            return
          }
          const res = await api.uploadImage(formData)
          self.newImage.img_name = res.data.data.img_name
          self.newImage.img_path = res.data.data.file_path
          self.disableAddButton = false
        }
      }
    },
    async handleVisibleSwitch (image) {
      await api.editBannerImage(image)
    },
    async deleteImage (imageId) {
      await this.$confirm('Sure to delete this Image? ', 'Delete Banner Image', 'warning', false)
      await api.deleteBannerImage(imageId)
      const res = await api.getBannerImage()
      this.bannerImageList = res.data.data
    }
  }
}
</script>

<style scoped lang="scss">
  .banner-images{
    display: flex;
    overflow-x: auto;
  }
  .banner-preview{
    margin-top: 10px;
    margin-right: 10px;
    width: 400px;
    height: auto;
  }
</style>
