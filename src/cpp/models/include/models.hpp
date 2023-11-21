#ifndef _MODELS_
#define _MODELS_

#include <map>
#include <stdexcept>
#include <string>

class NGramModel {
    private:
        uint8_t N;

    public:
        /**
         * Constructor for the N-Gram model. For now, this model will only
         * process N-Grams for values of N between 1 and 255.
        */
        NGramModel(uint8_t N);
        
        /**
         * This function takes in a set of training data and evaluates the 
         * N-Gram probabilities to construct the model.
         */        
        void Train();

        /**
         * This function takes the model resulting from the training sequence
         * and evaluates it against a set of validation data.
        */
        void Verify();

        /**
         * This function will generate a random sentence 
        */
        void Evaluate();
        void RandomSentence();

};



#endif