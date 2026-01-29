// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalRecord {
    struct Record {
        string patientId;
        string diseaseType;
        string prediction;
        string dataHash;
        string imageHash;
        uint256 timestamp;
        address hospital;
    }
    
    mapping(uint256 => Record) public records;
    uint256 public recordCount;
    
    event RecordAdded(
        uint256 indexed recordId,
        string patientId,
        string diseaseType,
        string prediction,
        uint256 timestamp
    );
    
    function addRecord(
        string memory _patientId,
        string memory _diseaseType,
        string memory _prediction,
        string memory _dataHash,
        string memory _imageHash
    ) public returns (uint256) {
        recordCount++;
        
        records[recordCount] = Record(
            _patientId,
            _diseaseType,
            _prediction,
            _dataHash,
            _imageHash,
            block.timestamp,
            msg.sender
        );
        
        emit RecordAdded(
            recordCount,
            _patientId,
            _diseaseType,
            _prediction,
            block.timestamp
        );
        
        return recordCount;
    }
    
    function getRecord(uint256 _recordId) public view returns (
        string memory patientId,
        string memory diseaseType,
        string memory prediction,
        string memory dataHash,
        string memory imageHash,
        uint256 timestamp,
        address hospital
    ) {
        Record memory record = records[_recordId];
        return (
            record.patientId,
            record.diseaseType,
            record.prediction,
            record.dataHash,
            record.imageHash,
            record.timestamp,
            record.hospital
        );
    }
}