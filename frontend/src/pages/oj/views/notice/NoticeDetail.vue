<template>
  <div>
    <div class="list-btn">
      <b-button
        class="border-0"
        variant="outline-dark"
      >
        <b-icon icon="list"></b-icon>목록
      </b-button>
    </div>

    <b-card border-variant="light">

      <template slot="header" class="header">
        <h4 class="title">SKKU Coding Platform 모의대회</h4>
        <h6 class="date">2021-02-08</h6>
      </template>

      <b-card-text>
        <pre>
          일시 : 1/4(월) - 1/10(일)
          참여 방법 : 상단의 'SKKU Coding Platform 모의대회' 클릭 후 참여
          참여 혜택 : 스타벅스 5000원 상품권 증정
          참여 조건 : 한 문제 이상 풀기

          문의 및 건의 :http://pf.kakao.com/_UKraK/chat
          (성균관대학교 코딩 플랫폼 개발 및 발전을 위한 건의 환영합니다)
        </pre>
      </b-card-text>

      <div>
        <b-table-simple>
          <b-tr>
            <b-td class="page-updown"><a href="#"><b-icon class="mr-2" icon="chevron-up"></b-icon>Previous</a></b-td>
            <b-td><a href="#">SKKU Coding Platform 모의대회</a></b-td>
          </b-tr>
          <b-tr>
            <b-td class="page-updown"><a href="#"><b-icon class="mr-2" icon="chevron-down"></b-icon>Next</a></b-td>
            <b-td><a href="#">SKKU Coding Platform 모의대회 솔루션 및 결과</a></b-td>
          </b-tr>
        </b-table-simple>
      </div>

    </b-card>
  </div>
</template>



<style>
  .list-btn{
    display: flex;
    justify-content: flex-end;
  }
  .title{
    float:left;
    margin:0;
  }
  .date{
    float:right;
    margin:5px 0 0 0;
  }
  .header{
    overflow:hidden;
  }
  .page-updown{
    width:130px;
  }
</style>