'use client';

import React, { useRef } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { ComponentContent, ComponentStyles } from '../../types';

interface HeroIntroScrollProps {
  content: ComponentContent;
  styles?: ComponentStyles;
  isPreview?: boolean;
}

export default function HeroIntroScroll({ content, styles, isPreview = false }: HeroIntroScrollProps) {
  const { title, description, image, button } = content;
  const ref = useRef(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start start', 'end start'],
  });

  const yTitle = useSpring(useTransform(scrollYProgress, [0, 0.35], [400, 0]), {
    stiffness: 90,
    damping: 18,
  });

  const scale = useSpring(useTransform(scrollYProgress, [0, 0.75], [1, 1.25]), {
    stiffness: 80,
    damping: 20,
  });

  const opacityIn = useTransform(scrollYProgress, [0.36, 0.45], [0, 1]);
  const opacityOut = useTransform(scrollYProgress, [0.45, 0.5], [1, 1]);

  const opacityText = useTransform(scrollYProgress, (value: number) => {
    if (value < 0.36) return 0;
    if (value >= 0.5) return 1;
    return opacityIn.get() * opacityOut.get();
  });

  const shadowOpacity = useTransform(scrollYProgress, [0.01, 0.1], [0, 0.5]);

  // Si estamos en preview, no usar animaciones
  if (isPreview) {
    return (
      <div className='relative h-[240vh] w-full'>
        <div className='sticky top-0 h-screen w-full'>
          <div className='absolute inset-0 overflow-hidden'>
            <div className='absolute inset-0 z-0 flex items-center justify-center bg-black'>
              {image && (
                <img
                  src={image}
                  alt="Hero background"
                  className='object-cover w-full h-full'
                />
              )}
            </div>

            <div className="absolute inset-0 z-10 bg-black/50 pointer-events-none" />

            <div className="absolute inset-0 z-10 flex items-center">
              <div className="max-w-7xl px-6 w-full mx-auto">
                <h1 className='max-w-md text-[56px] leading-[64px] font-bold text-white mb-8'>
                  {title || 'Título principal'}
                </h1>

                <div className='max-w-xl'>
                  <p className='text-lg text-white mb-8'>
                    {description || 'Descripción del hero'}
                  </p>
                  {button && (
                    <a 
                      href={button.href || '#'} 
                      className="inline-block px-6 py-3 bg-white text-black font-semibold rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      {button.label || 'Botón'}
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div ref={ref} className='relative h-[240vh] w-full'>
      <div className='sticky top-0 h-screen w-full'>
        <div className='absolute inset-0 overflow-hidden'>
          <motion.div 
            style={{ scale }} 
            className='absolute inset-0 z-0 flex items-center justify-center bg-black'
          >
            {image && (
              <img
                src={image}
                alt="Hero background"
                className='object-cover w-full h-full'
              />
            )}
          </motion.div>

          <motion.div
            style={{ opacity: shadowOpacity }}
            className="absolute inset-0 z-10 bg-black/50 pointer-events-none"
          />

          <div className="absolute inset-0 z-10 flex items-center">
            <div className="max-w-7xl px-6 w-full mx-auto">
              <motion.h1
                style={{ y: yTitle }}
                className='max-w-md text-[56px] leading-[64px] font-bold text-white mb-8'
              >
                {title || 'Título principal'}
              </motion.h1>

              <motion.div
                style={{ opacity: opacityText }}
                className='max-w-xl'
              >
                <p className='text-lg text-white mb-8'>
                  {description || 'Descripción del hero'}
                </p>
                {button && (
                  <a 
                    href={button.href || '#'} 
                    className="inline-block px-6 py-3 bg-white text-black font-semibold rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    {button.label || 'Botón'}
                  </a>
                )}
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 