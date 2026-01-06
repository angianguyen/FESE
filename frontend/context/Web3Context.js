/**
 * Web3 Context Provider for StreamCredit
 * Handles wallet connection and contract interactions
 */

'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { ethers } from 'ethers';
import { STREAM_CREDIT_ABI } from '../config/abi';

// Contract addresses from deployed-addresses-mock.json (MockVerifier - for testing)
// For production with real ZK proofs, use deployed-addresses.json with Groth16Verifier
const CONTRACTS = {
  // MockVerifier deployment (for demo - always accepts proofs)
  streamCredit: '0xCF2a831E6D389974992F9b4fc20f9B45fDd95475',
  mockUSDC: '0x25117A7cd454E8C285553f0629696a28bAB3356c',
  mockVerifier: '0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF',
  
  // Real Verifier deployment (requires real ZK proofs)
  // streamCredit: '0x2F90F76F1D3fCD66c92Ab00DCDa1e7C5A61200b9',
  // mockUSDC: '0x2b1561Ef1C3bE02180A32E7aae6A7566Ed8F27a8',
  // groth16Verifier: '0xCAecEC1e406B524fDa7C29424AEcD5dB6FBa896b'
};

// Sepolia Chain ID
const SEPOLIA_CHAIN_ID = 11155111;
const SEPOLIA_CHAIN_ID_HEX = '0xaa36a7';

const Web3Context = createContext(null);

export function useWeb3() {
  const context = useContext(Web3Context);
  if (!context) {
    throw new Error('useWeb3 must be used within a Web3Provider');
  }
  return context;
}

export function Web3Provider({ children }) {
  const [account, setAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [chainId, setChainId] = useState(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);
  const [streamCreditContract, setStreamCreditContract] = useState(null);
  const [allAccounts, setAllAccounts] = useState([]); // Track all connected accounts

  // Check if MetaMask is installed
  const isMetaMaskInstalled = typeof window !== 'undefined' && window.ethereum;

  // Initialize provider on mount - but DON'T auto-connect
  useEffect(() => {
    if (isMetaMaskInstalled) {
      const ethersProvider = new ethers.BrowserProvider(window.ethereum);
      setProvider(ethersProvider);

      // Listen for account changes (when user switches in MetaMask)
      window.ethereum.on('accountsChanged', (accounts) => {
        console.log('MetaMask accounts changed:', accounts);
        if (accounts.length === 0) {
          disconnectWallet();
        } else {
          setAccount(accounts[0]);
          setAllAccounts(accounts);
        }
      });

      // Listen for chain changes
      window.ethereum.on('chainChanged', (newChainId) => {
        setChainId(parseInt(newChainId, 16));
        // Don't reload - just update state
        console.log('Chain changed to:', parseInt(newChainId, 16));
      });

      // DON'T auto-connect - let user click "Connect Wallet" button
      // This allows testing with different wallets
    }
  }, []);

  // Initialize contract when signer is available
  useEffect(() => {
    if (signer) {
      const contract = new ethers.Contract(
        CONTRACTS.streamCredit,
        STREAM_CREDIT_ABI,
        signer
      );
      setStreamCreditContract(contract);
    }
  }, [signer]);

  // Update signer when account changes
  useEffect(() => {
    if (provider && account) {
      provider.getSigner().then(setSigner);
    }
  }, [provider, account]);

  // Connect wallet
  const connectWallet = useCallback(async () => {
    if (!isMetaMaskInstalled) {
      setError('MetaMask is not installed. Please install it from metamask.io');
      return false;
    }

    setIsConnecting(true);
    setError(null);

    try {
      // Request accounts
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });

      if (accounts.length === 0) {
        throw new Error('No accounts found');
      }

      setAccount(accounts[0]);

      // Check chain
      const chainIdHex = await window.ethereum.request({ method: 'eth_chainId' });
      const currentChainId = parseInt(chainIdHex, 16);
      setChainId(currentChainId);

      // Switch to Sepolia if not on it
      if (currentChainId !== SEPOLIA_CHAIN_ID) {
        try {
          await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: SEPOLIA_CHAIN_ID_HEX }]
          });
        } catch (switchError) {
          // Chain not added, try to add it
          if (switchError.code === 4902) {
            await window.ethereum.request({
              method: 'wallet_addEthereumChain',
              params: [{
                chainId: SEPOLIA_CHAIN_ID_HEX,
                chainName: 'Sepolia Testnet',
                nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                rpcUrls: ['https://rpc.sepolia.org'],
                blockExplorerUrls: ['https://sepolia.etherscan.io']
              }]
            });
          } else {
            throw switchError;
          }
        }
      }

      setIsConnecting(false);
      return true;
    } catch (err) {
      console.error('Failed to connect wallet:', err);
      setError(err.message || 'Failed to connect wallet');
      setIsConnecting(false);
      return false;
    }
  }, [isMetaMaskInstalled]);

  // Disconnect wallet
  const disconnectWallet = useCallback(() => {
    setAccount(null);
    setSigner(null);
    setStreamCreditContract(null);
    setAllAccounts([]);
    console.log('Wallet disconnected');
  }, []);

  // Switch to a different account - opens MetaMask account selector
  const switchAccount = useCallback(async () => {
    if (!isMetaMaskInstalled) {
      setError('MetaMask is not installed');
      return false;
    }

    try {
      // Request wallet_requestPermissions to force MetaMask to show account picker
      await window.ethereum.request({
        method: 'wallet_requestPermissions',
        params: [{ eth_accounts: {} }]
      });

      // Get the newly selected account
      const accounts = await window.ethereum.request({
        method: 'eth_accounts'
      });

      if (accounts.length > 0) {
        setAccount(accounts[0]);
        setAllAccounts(accounts);
        console.log('Switched to account:', accounts[0]);
        return true;
      }
      return false;
    } catch (err) {
      console.error('Failed to switch account:', err);
      setError(err.message || 'Failed to switch account');
      return false;
    }
  }, [isMetaMaskInstalled]);

  // Get account info from contract
  const getAccountInfo = useCallback(async () => {
    if (!streamCreditContract || !account) return null;

    try {
      const info = await streamCreditContract.getAccountInfo(account);
      return {
        creditLimit: ethers.formatUnits(info._creditLimit, 6), // USDC has 6 decimals
        borrowed: ethers.formatUnits(info._borrowed, 6),
        available: ethers.formatUnits(info._available, 6)
      };
    } catch (err) {
      console.error('Failed to get account info:', err);
      return null;
    }
  }, [streamCreditContract, account]);

  // Submit ZK proof to contract
  const submitZKProof = useCallback(async (proof, publicSignals, revenue) => {
    if (!streamCreditContract) {
      throw new Error('Contract not initialized. Please connect wallet first.');
    }

    try {
      // For MockVerifier, we can send any valid uint256 values
      // The proof format from mock API uses hex strings, convert to BigInt
      const parseHexOrNumber = (val) => {
        if (typeof val === 'string' && val.startsWith('0x')) {
          // Truncate to valid uint256 range
          return BigInt(val.slice(0, 66));
        }
        return BigInt(val || '0');
      };

      // Parse proof components
      const a = [
        parseHexOrNumber(proof.pi_a?.[0] || '1'),
        parseHexOrNumber(proof.pi_a?.[1] || '2')
      ];
      const b = [
        [
          parseHexOrNumber(proof.pi_b?.[0]?.[0] || '1'),
          parseHexOrNumber(proof.pi_b?.[0]?.[1] || '2')
        ],
        [
          parseHexOrNumber(proof.pi_b?.[1]?.[0] || '3'),
          parseHexOrNumber(proof.pi_b?.[1]?.[1] || '4')
        ]
      ];
      const c = [
        parseHexOrNumber(proof.pi_c?.[0] || '1'),
        parseHexOrNumber(proof.pi_c?.[1] || '2')
      ];
      
      // input[0] should be 1 (isValid = true)
      const input = [BigInt(1)];

      // Convert revenue to USDC format (6 decimals)
      const revenueInUSDC = ethers.parseUnits(revenue.toString(), 6);

      console.log('Submitting ZK proof to contract...');
      console.log('a:', a);
      console.log('b:', b);
      console.log('c:', c);
      console.log('input:', input);
      console.log('revenue:', revenueInUSDC.toString());

      const tx = await streamCreditContract.verifyAndUpdateCredit(
        a, b, c, input, revenueInUSDC
      );

      console.log('Transaction submitted:', tx.hash);
      
      // Wait for confirmation
      const receipt = await tx.wait();
      console.log('Transaction confirmed:', receipt);

      return {
        success: true,
        txHash: tx.hash,
        receipt
      };
    } catch (err) {
      console.error('Failed to submit ZK proof:', err);
      throw err;
    }
  }, [streamCreditContract]);

  // Borrow from contract
  const borrow = useCallback(async (amount) => {
    if (!streamCreditContract) {
      throw new Error('Contract not initialized');
    }

    try {
      const amountInUSDC = ethers.parseUnits(amount.toString(), 6);
      const tx = await streamCreditContract.borrow(amountInUSDC);
      const receipt = await tx.wait();
      
      return {
        success: true,
        txHash: tx.hash,
        receipt
      };
    } catch (err) {
      console.error('Failed to borrow:', err);
      throw err;
    }
  }, [streamCreditContract]);

  // Repay to contract
  const repay = useCallback(async (amount) => {
    if (!streamCreditContract) {
      throw new Error('Contract not initialized');
    }

    try {
      const amountInUSDC = ethers.parseUnits(amount.toString(), 6);
      const tx = await streamCreditContract.repay(amountInUSDC);
      const receipt = await tx.wait();
      
      return {
        success: true,
        txHash: tx.hash,
        receipt
      };
    } catch (err) {
      console.error('Failed to repay:', err);
      throw err;
    }
  }, [streamCreditContract]);

  const value = {
    // State
    account,
    allAccounts,
    chainId,
    isConnecting,
    error,
    isConnected: !!account,
    isOnSepolia: chainId === SEPOLIA_CHAIN_ID,
    
    // Methods
    connectWallet,
    disconnectWallet,
    switchAccount,
    getAccountInfo,
    submitZKProof,
    borrow,
    repay,
    
    // Contract
    streamCreditContract,
    
    // Constants
    contracts: CONTRACTS
  };

  return (
    <Web3Context.Provider value={value}>
      {children}
    </Web3Context.Provider>
  );
}
