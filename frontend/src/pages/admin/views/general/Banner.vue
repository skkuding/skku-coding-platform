<template>
    <div class="view">
        <Panel title="Current Images">
            <div class="banner-images">
                <b-img
                    :src="require('@/assets/banner1.png')"
                    rounded
                    class="banner-preview"
                />
                <b-img
                    :src="require('@/assets/banner2.png')"
                    rounded
                    class="banner-preview"
                />
                <b-img
                    :src="require('@/assets/banner3.png')"
                    rounded
                    class="banner-preview"
                />
            </div>
            <b-table
                style="margin-top: 20px;"
                :items="bannerImageList"
                :fields="bannerImageListFields"
            >
                <template #cell(options)="">
                    <icon-btn
                        name="Delete"
                        icon="trash"
                    />
                </template>
            </b-table>
        </Panel>
        <Panel title="Import New Image">
            <div>* Banner image size: 2000 * 613</div>
            <b-form-file
                multiple
                v-model="newImage"
                accept="image/*"
                style="margin-top: 10px;"
            >
                <template slot="file-name" slot-scope="{names}">
                    <b-badge
                        v-for="(name, index) in names"
                        :key="index"
                        style="font-size: 14px; margin-right: 10px;"
                    >
                        <span v-if="index < 4"> {{ names[index] }} </span>
                    </b-badge>
                    <b-badge v-if="names.length > 4" style="font-size: 14px;"> + {{ names.length - 4 + ' More files' }} </b-badge>
                </template>
            </b-form-file>
            <b-button
                variant="primary"
                size="sm"
                style="margin-top: 10px;"
            >Save</b-button>
        </Panel>
    </div>
</template>

<script>
export default {
  name: 'Banner',
  data () {
    return {
      bannerImageList: [
        { title: 'Banner1', size: '2000*613', createTime: '2021-12-6 17:43:11' },
        { title: 'Banner2', size: '2000*613', createTime: '2021-12-7 12:33:15' },
        { title: 'Banner3', size: '2000*613', createTime: '2021-12-7 12:34:11' }
      ],
      bannerImageListFields: [
        { key: 'title', label: 'Title' },
        { key: 'size', label: 'Size' },
        { key: 'createTime', label: 'Create Time' },
        { key: 'options', label: 'Options' }
      ],
      newImage: []
    }
  },
  async mounted () {
  },
  methods: {
  }
}
</script>

<style scoped lang="scss">
    .banner-images{
        display:flex;
        overflow-x: auto;
    }
    .banner-preview{
        margin-top: 10px;
        margin-right: 10px;
        width: 400px;
        height: auto;
    }

</style>
