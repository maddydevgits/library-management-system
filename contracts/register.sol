// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract register {
  
  uint[] rollNos;
  uint[] passwords;
  address[] studentWallets;
  string[] studentNames;

  function registerStudent(address wallet,string memory name,uint rollNo,uint password) public {
    rollNos.push(rollNo);
    passwords.push(password);
    studentWallets.push(wallet);
    studentNames.push(name);
  }

  function viewStudents() public view returns (uint[] memory, uint[] memory, address[] memory, string[] memory) {
    return (rollNos,passwords,studentWallets,studentNames);
  }

  function loginStudent(address wallet,uint password) public view returns(bool) {

    uint i;
    for(i=0;i<studentWallets.length;i++) {
      if(studentWallets[i]==wallet && password==passwords[i]) {
        return true;
      }
    }
    return false;
  }
}
