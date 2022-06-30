// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract lms {
  
  string[] book_names;
  uint[] book_ids;
  uint[] book_counts;
  uint[] book_a;

  uint[] _brollNo;
  uint[] _bbookId;
  bool[] _bstatus;

  function addBook(string memory bookName, uint bookId, uint bookCount) public {
      
      book_names.push(bookName);
      book_ids.push(bookId);
      book_counts.push(bookCount);
      book_a.push(bookCount);
  }

  function viewBooks() public view returns (string[] memory, uint[] memory, uint[] memory,uint[] memory) {
      return(book_names,book_ids,book_counts,book_a);
  }

  function allocateBook(uint rollNo, uint bookId) public {

      uint i;

      for(i=0;i<book_names.length;i++) {
          if(book_ids[i]==bookId) {
              book_a[i]-=1;
          }
      }
      _brollNo.push(rollNo);
      _bbookId.push(bookId);
      _bstatus.push(true);


  }

  function returnBook(uint rollNo, uint bookId) public {

      uint i;

      for(i=0;i<_brollNo.length;i++) {
          if(_brollNo[i]==rollNo && _bbookId[i]==bookId) {
              _bstatus[i]=false;
          }
      }

      for(i=0;i<book_names.length;i++) {
          if(book_ids[i]==bookId) {
              book_a[i]+=1;
          }
      }
  }

  function listBooks() public view returns(uint[] memory, uint[] memory, bool[] memory) {
      return (_brollNo,_bbookId,_bstatus);
  }

  
}
