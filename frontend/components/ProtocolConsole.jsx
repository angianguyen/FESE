'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ethers } from 'ethers';
import { 
  CheckCircle2, 
  AlertTriangle, 
  Lock, 
  TrendingUp,
  Terminal,
  RefreshCw,
  ArrowLeft,
  Activity
} from 'lucide-react';
import { useWeb3 } from '../context/Web3Context';
import { API_ENDPOINTS } from '../config/constants';

const ProtocolConsole = ({ onBack }) => {
  const { account, streamCreditContract, isOnSepolia, chainId } = useWeb3();
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [revenueData, setRevenueData] = useState(null);
  const [riskStatus, setRiskStatus] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingProof, setIsGeneratingProof] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [creditLimit, setCreditLimit] = useState(5000);
  const [availableCredit, setAvailableCredit] = useState(3800);
  const [consoleLog, setConsoleLog] = useState([]);
  const consoleRef = useRef(null);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString('en-US', { hour12: false });
    setConsoleLog(prev => [...prev, { timestamp, message, type }]);
  };

  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [consoleLog]);

  useEffect(() => {
    addLog('Console initialized. Waiting for user input...', 'system');
    if (account) {
      addLog(`Wallet connected: ${account.slice(0, 6)}...${account.slice(-4)}`, 'success');
      loadAccountInfo();
    }
  }, [account]);

  const loadAccountInfo = async () => {
    if (!streamCreditContract || !account) return;
    
    try {
      const [limit, borrowed, available] = await streamCreditContract.getAccountInfo(account);
      setCreditLimit(Number(limit));
      setAvailableCredit(Number(available));
      addLog(`Credit info loaded: ${Number(limit).toLocaleString()} USDC limit`, 'system');
    } catch (error) {
      console.error('Failed to load account info:', error);
    }
  };

  const handleScenarioSelect = async (scenario) => {
    setSelectedScenario(scenario);
    setIsAnalyzing(true);
    setRevenueData(null);
    setRiskStatus(null);
    
    addLog(`Selected scenario: ${scenario}`, 'user');
    addLog('Fetching order data from Mock API...', 'info');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      if (scenario === 'honest') {
        setRevenueData('$50,000');
        setRiskStatus({ level: 'LOW', score: '8%', message: 'Dữ liệu bán hàng tự nhiên tuân theo quy luật Benford.' });
        addLog('✓ Data analysis complete: Revenue = $50,000', 'success');
        addLog('✓ Benford Score = 8% (Low risk)', 'success');
      } else {
        setRevenueData('$100,000');
        setRiskStatus({ level: 'HIGH', score: '45%', message: 'Phát hiện số tròn, lặp lại (có dấu hiệu Wash Trading).' });
        addLog('✓ Data analysis complete: Revenue = $100,000', 'warning');
        addLog('⚠ Benford Score = 45% (High risk - Wash Trading detected)', 'error');
      }
    } catch (error) {
      addLog(`✗ Error: ${error.message}`, 'error');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleGenerateProof = async () => {
    setIsGeneratingProof(true);
    addLog('Generating Zero-Knowledge Proof...', 'info');
    addLog('Using Groth16 proving system (SnarkJS)', 'system');

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      addLog('✓ ZK Proof generated successfully', 'success');
      addLog('Proof hash: 0x7f3a...c8d2', 'system');
    } catch (error) {
      addLog(`✗ Proof generation failed: ${error.message}`, 'error');
    } finally {
      setIsGeneratingProof(false);
    }
  };

  const handleSubmit = async () => {
    if (riskStatus?.level === 'HIGH') {
      addLog('✗ Transaction rejected: High fraud risk detected', 'error');
      return;
    }

    if (!account) {
      addLog('✗ Please connect wallet first', 'error');
      return;
    }

    if (!isOnSepolia) {
      addLog(`✗ Please switch to Sepolia network (Current: Chain ID ${chainId})`, 'error');
      return;
    }

    setIsSubmitting(true);
    addLog('Submitting verification to Smart Contract...', 'info');
    addLog(`Contract: StreamCredit.sol (Sepolia)`, 'system');
    addLog(`From: ${account.slice(0, 6)}...${account.slice(-4)}`, 'system');

    try {
      // Dummy ZK proof (MockVerifier accepts any proof)
      const dummyProof = {
        a: [1, 2],
        b: [[1, 2], [1, 2]],
        c: [1, 2],
        input: [1]
      };

      const revenueValue = selectedScenario === 'honest' ? 50000 : 100000;

      addLog('Calling verifyAndUpdateCredit()...', 'info');
      
      const tx = await streamCreditContract.verifyAndUpdateCredit(
        dummyProof.a,
        dummyProof.b,
        dummyProof.c,
        dummyProof.input,
        revenueValue
      );

      addLog(`✓ Transaction sent: ${tx.hash}`, 'success');
      addLog('Waiting for confirmation...', 'info');

      const receipt = await tx.wait();
      
      addLog(`✓ Transaction confirmed in block ${receipt.blockNumber}`, 'success');
      addLog(`Gas used: ${ethers.formatEther(receipt.gasUsed * receipt.gasPrice)} ETH`, 'system');
      addLog(`View on Etherscan: https://sepolia.etherscan.io/tx/${tx.hash}`, 'system');

      // Update UI from contract
      const [newCreditLimit, borrowed, available] = await streamCreditContract.getAccountInfo(account);
      setCreditLimit(Number(newCreditLimit));
      setAvailableCredit(Number(available));
      
      addLog(`✓ Credit Limit updated: ${Number(newCreditLimit).toLocaleString()} USDC`, 'success');
    } catch (error) {
      console.error('Submit error:', error);
      const errorMessage = error.reason || error.message || 'Unknown error';
      addLog(`✗ Transaction failed: ${errorMessage}`, 'error');
      
      if (error.code === 'ACTION_REJECTED') {
        addLog('User rejected transaction in MetaMask', 'error');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBorrow = async (amount) => {
    if (!account || !isOnSepolia) {
      addLog(`✗ Please connect wallet to Sepolia (Current: Chain ID ${chainId})`, 'error');
      return;
    }

    if (amount > availableCredit) {
      addLog(`✗ Cannot borrow ${amount.toLocaleString()}: Exceeds available credit`, 'error');
      return;
    }

    addLog(`Borrowing ${amount.toLocaleString()} USDC...`, 'info');
    
    try {
      const tx = await streamCreditContract.borrow(amount);
      addLog(`✓ Transaction sent: ${tx.hash}`, 'success');
      
      const receipt = await tx.wait();
      addLog(`✓ Borrowed ${amount.toLocaleString()} USDC`, 'success');
      addLog(`View: https://sepolia.etherscan.io/tx/${tx.hash}`, 'system');

      // Update from contract
      const [, , available] = await streamCreditContract.getAccountInfo(account);
      setAvailableCredit(Number(available));
    } catch (error) {
      const errorMessage = error.reason || error.message || 'Unknown error';
      addLog(`✗ Borrow failed: ${errorMessage}`, 'error');
    }
  };

  const handleRepay = async () => {
    if (!account || !isOnSepolia) {
      addLog(`✗ Please connect wallet to Sepolia (Current: Chain ID ${chainId})`, 'error');
      return;
    }

    const borrowed = creditLimit - availableCredit;
    if (borrowed <= 0) {
      addLog('✗ No outstanding debt to repay', 'error');
      return;
    }

    addLog(`Repaying ${borrowed.toLocaleString()} USDC...`, 'info');
    
    try {
      const tx = await streamCreditContract.repay(borrowed);
      addLog(`✓ Transaction sent: ${tx.hash}`, 'success');
      
      const receipt = await tx.wait();
      addLog(`✓ Repaid ${borrowed.toLocaleString()} USDC`, 'success');
      addLog(`View: https://sepolia.etherscan.io/tx/${tx.hash}`, 'system');

      // Update from contract
      const [, , available] = await streamCreditContract.getAccountInfo(account);
      setAvailableCredit(Number(available));
    } catch (error) {
      const errorMessage = error.reason || error.message || 'Unknown error';
      addLog(`✗ Repay failed: ${errorMessage}`, 'error');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 text-slate-100">
      {/* Header */}
      <div className="border-b border-slate-800/60 bg-slate-950/80 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <div className="flex items-center gap-3">
                <Terminal className="text-cyan-400" size={24} />
                <h1 className="text-2xl font-bold">Protocol Console</h1>
              </div>
              <p className="text-sm text-slate-400 mt-0.5">
                Tương tác trực tiếp với Smart Contract & ZK Verifier
              </p>
            </div>
          </div>
          <div className="text-xs text-slate-500 bg-slate-800/50 px-3 py-1.5 rounded-full border border-slate-700">
            v0.1.0 beta
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-[1600px] mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Main Actions */}
          <div className="lg:col-span-2 space-y-6">
            {/* Step 1: Choose Data Source */}
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <h2 className="text-lg font-semibold">Chọn nguồn dữ liệu</h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Honest Merchant Card */}
                <button
                  onClick={() => handleScenarioSelect('honest')}
                  className={`glass-panel p-6 rounded-xl text-left transition-all ${
                    selectedScenario === 'honest'
                      ? 'border-emerald-500/50 bg-emerald-500/10'
                      : 'border-slate-700/50 hover:border-emerald-500/30'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
                      <CheckCircle2 className="text-emerald-400" size={24} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white mb-2">Honest Merchant</h3>
                      <p className="text-sm text-slate-400">
                        Dữ liệu bán hàng tự nhiên tuân theo quy luật Benford.
                      </p>
                    </div>
                  </div>
                </button>

                {/* Wash Trader Card */}
                <button
                  onClick={() => handleScenarioSelect('fraud')}
                  className={`glass-panel p-6 rounded-xl text-left transition-all ${
                    selectedScenario === 'fraud'
                      ? 'border-red-500/50 bg-red-500/10'
                      : 'border-slate-700/50 hover:border-red-500/30'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
                      <AlertTriangle className="text-red-400" size={24} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white mb-2">Wash Trader</h3>
                      <p className="text-sm text-slate-400">
                        Điều khiển thao túng volume (số tròn, lặp lại bất thường).
                      </p>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            {/* Step 2: Analysis & Proof Generation */}
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <h2 className="text-lg font-semibold">Phân tích & Tạo Proof</h2>
              </div>

              <div className="glass-panel p-6 rounded-xl">
                <div className="grid grid-cols-2 gap-6 mb-6">
                  {/* Revenue */}
                  <div>
                    <div className="text-sm text-slate-400 mb-2">Doanh thu phát hiện</div>
                    <div className="text-2xl font-bold">
                      {isAnalyzing ? (
                        <RefreshCw className="animate-spin text-slate-500" size={20} />
                      ) : revenueData || '- - -'}
                    </div>
                  </div>

                  {/* Risk Status */}
                  <div>
                    <div className="text-sm text-slate-400 mb-2">Trạng thái rủi ro</div>
                    <div className="text-2xl font-bold">
                      {isAnalyzing ? (
                        <RefreshCw className="animate-spin text-slate-500" size={20} />
                      ) : riskStatus ? (
                        <span className={riskStatus.level === 'LOW' ? 'text-emerald-400' : 'text-red-400'}>
                          {riskStatus.score}
                        </span>
                      ) : '- - -'}
                    </div>
                  </div>
                </div>

                {riskStatus && (
                  <div className={`p-4 rounded-lg mb-6 ${
                    riskStatus.level === 'LOW' 
                      ? 'bg-emerald-500/10 border border-emerald-500/30' 
                      : 'bg-red-500/10 border border-red-500/30'
                  }`}>
                    <p className="text-sm">{riskStatus.message}</p>
                  </div>
                )}

                <div className="flex gap-3">
                  <button
                    onClick={handleGenerateProof}
                    disabled={!revenueData || isGeneratingProof}
                    className="flex-1 px-4 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                  >
                    {isGeneratingProof ? (
                      <>
                        <RefreshCw className="animate-spin" size={16} />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Lock size={16} />
                        Generate ZK Proof
                      </>
                    )}
                  </button>

                  <button
                    onClick={handleSubmit}
                    disabled={!revenueData || isSubmitting || riskStatus?.level === 'HIGH'}
                    className="flex-1 px-4 py-3 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                  >
                    {isSubmitting ? (
                      <>
                        <RefreshCw className="animate-spin" size={16} />
                        Submitting...
                      </>
                    ) : (
                      <>
                        <TrendingUp size={16} />
                        Submit On-Chain
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Position Info */}
          <div className="space-y-6">
            {/* Your Position */}
            <div className="glass-panel p-6 rounded-xl sticky top-24">
              <h3 className="text-sm font-semibold text-slate-400 mb-4 uppercase tracking-wider">
                Your Position
              </h3>

              <div className="space-y-4">
                {/* Credit Limit */}
                <div>
                  <div className="flex justify-between items-end mb-2">
                    <div>
                      <div className="text-sm text-slate-400">Credit Limit</div>
                      <div className="text-3xl font-bold">${creditLimit.toLocaleString()}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-slate-400">Available</div>
                      <div className="text-xl font-bold text-emerald-400">
                        ${availableCredit.toLocaleString()}
                      </div>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-500 to-blue-600 transition-all duration-500"
                      style={{ width: `${(availableCredit / creditLimit) * 100}%` }}
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4">
                  <button
                    onClick={() => handleBorrow(5000)}
                    disabled={availableCredit < 5000}
                    className="flex-1 px-4 py-3 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/30 text-cyan-400 font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Borrow
                  </button>
                  <button
                    onClick={handleRepay}
                    disabled={availableCredit >= creditLimit}
                    className="flex-1 px-4 py-3 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 text-purple-400 font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Repay
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Console Log */}
        <div className="mt-6 glass-panel rounded-xl overflow-hidden">
          <div className="bg-slate-900/80 px-4 py-2 flex items-center gap-2 border-b border-slate-700/50">
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/80" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
              <div className="w-3 h-3 rounded-full bg-green-500/80" />
            </div>
            <div className="text-xs text-slate-500 ml-2 flex items-center gap-2">
              <Terminal size={12} />
              console.log
            </div>
          </div>
          
          <div
            ref={consoleRef}
            className="bg-slate-950/50 p-4 font-mono text-xs h-64 overflow-y-auto"
          >
            {consoleLog.length === 0 ? (
              <div className="text-slate-600 italic">Waiting for interaction...</div>
            ) : (
              consoleLog.map((log, idx) => (
                <div key={idx} className="mb-1">
                  <span className="text-slate-500">[{log.timestamp} AM]</span>
                  {' '}
                  <span className={
                    log.type === 'error' ? 'text-red-400' :
                    log.type === 'warning' ? 'text-yellow-400' :
                    log.type === 'success' ? 'text-emerald-400' :
                    log.type === 'system' ? 'text-cyan-400' :
                    'text-slate-300'
                  }>
                    {log.message}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProtocolConsole;
