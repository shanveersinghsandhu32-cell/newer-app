// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract CertificateRegistry {
    address public owner;
    mapping(address => bool) public authorizedIssuers;

    struct Cert {
        bytes32 certHash;
        address issuer;
        uint256 issueDate;
        string metadataURI;
        bool revoked;
    }

    mapping(bytes32 => Cert) private certificates;

    event Issued(bytes32 indexed certId, address indexed issuer, uint256 issueDate, string metadataURI);
    event Revoked(bytes32 indexed certId, address indexed revoker);

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    modifier onlyIssuer() {
        require(authorizedIssuers[msg.sender], "not an authorized issuer");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setIssuer(address _issuer, bool _allowed) external onlyOwner {
        authorizedIssuers[_issuer] = _allowed;
    }

    function issueCertificate(bytes32 certHash, string calldata metadataURI) external onlyIssuer {
        require(certificates[certHash].issueDate == 0, "certificate already issued");
        certificates[certHash] = Cert(certHash, msg.sender, block.timestamp, metadataURI, false);
        emit Issued(certHash, msg.sender, block.timestamp, metadataURI);
    }

    function revokeCertificate(bytes32 certHash) external {
        require(certificates[certHash].issueDate != 0, "certificate not found");
        require(certificates[certHash].issuer == msg.sender || msg.sender == owner, "not authorized to revoke");
        certificates[certHash].revoked = true;
        emit Revoked(certHash, msg.sender);
    }

    function getCertificate(bytes32 certHash) external view returns (
        bytes32, address, uint256, string memory, bool
    ) {
        Cert memory c = certificates[certHash];
        return (c.certHash, c.issuer, c.issueDate, c.metadataURI, c.revoked);
    }

    function isValid(bytes32 certHash) external view returns (bool) {
        Cert memory c = certificates[certHash];
        return (c.issueDate != 0 && !c.revoked);
    }
}
