<template>
  <div class="pagee">
    <div class="page-itm">
      <div class="page-btn">&lt;&lt;</div>
      <div class="page-btn">&lt;</div>
      <div class="page-btn">1</div>
      <div class="page-btn">&gt;</div>
      <div class="page-btn">&gt;&gt;</div>
    </div>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
.pagee {
  width: 95%;
  margin-right: 10%;
  margin-top: 10px;
  display: flex;
  justify-content: flex-end !important;
}

.page-itm {
  border-radius: 50rem !important;
  margin-left: 0.25rem;
  padding: 0.25rem 0.25rem 0.25rem 0;
  line-height: 1;
  display: flex;
  flex-direction: row;
}

.page-btn {
  width: 30px;
  height: 30px;
  text-align: center;
  line-height: 25px;
  margin-left: 0.25rem;
  border-radius: 5px !important;
  color: #bdbdbd;
  border: thin solid #bdbdbd;
  cursor: pointer;
}
</style>
