import Foundation

func getSecKeyAlgorithm() -> SecKeyAlgorithm {
    return SecKeyAlgorithm.eciesEncryptionStandardVariableIVX963SHA512AESGCM
}

func getSecKeyAlgorithmSizeInBits() -> Int {
    521
}

func saveData(_ data:Data, _ fileName: String) {
    let fileURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0].appendingPathComponent(fileName)

    do {
        try data.write(to: fileURL)
    } catch {
        print("Error saving data to file: \(error)")
    }
}

func generateTestData() {
    let params: [String: Any] = [
        kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
        kSecAttrKeySizeInBits as String: getSecKeyAlgorithmSizeInBits(),
        kSecPrivateKeyAttrs as String: [
            kSecAttrIsPermanent as String: true,
        ]
    ]

    var errorSecKeyCreateRandomKey: Unmanaged<CFError>?

    guard let privateKey = SecKeyCreateRandomKey(params as CFDictionary, &errorSecKeyCreateRandomKey) else {
        print("Error creating private key: \(errorSecKeyCreateRandomKey!.takeRetainedValue() as Error)")
        return
    }
    
    guard let publicKey = SecKeyCopyPublicKey(privateKey) else {
        print("Cannot get public key.")
        return
    }
    
    var errorPrivateSecKeyCopyExternalRepresentation: Unmanaged<CFError>?
    guard let privateKeyData = SecKeyCopyExternalRepresentation(privateKey, &errorPrivateSecKeyCopyExternalRepresentation) as Data? else {
        print("Error getting external representation of private key: \(errorPrivateSecKeyCopyExternalRepresentation!.takeRetainedValue() as Error)")
        return
    }
    
    var errorPublicSecKeyCopyExternalRepresentation: Unmanaged<CFError>?
    guard let publicKeyData = SecKeyCopyExternalRepresentation(publicKey, &errorPublicSecKeyCopyExternalRepresentation) as Data? else {
        print("Error getting external representation of public key: \(errorPublicSecKeyCopyExternalRepresentation!.takeRetainedValue() as Error)")
        return
    }
    
    let helloWorldString = "Hello World!"
    let helloWorldData = helloWorldString.data(using: .utf8)!
    
    var errorSecKeyCreateEncryptedData : Unmanaged<CFError>?
    guard let encrypted = SecKeyCreateEncryptedData(
            publicKey,
            getSecKeyAlgorithm(),
            helloWorldData as CFData,
            &errorSecKeyCreateEncryptedData
    ) else {
        print("Cannot encrypt: \(errorSecKeyCreateEncryptedData!.takeRetainedValue() as Error)")
        return
    }
    
    saveData(privateKeyData, "private_key.txt")
    saveData(publicKeyData, "public_key.txt")
    saveData(encrypted as Data, "encrypted.txt")

    print(helloWorldString)
}

generateTestData()
